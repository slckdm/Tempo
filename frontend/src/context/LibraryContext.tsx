import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";
import type { ReactNode } from "react";

import { ApiError } from "../api/client";
import { fetchTracks } from "../api/metadata";
import { completeUpload, createUpload, deleteUpload, putToPresigned } from "../api/uploads";
import { isAudioFile, resolveContentType } from "../lib/audioFiles";
import type { Track, UploadItem, UploadPhase } from "../types";
import { useAuth } from "./AuthContext";

interface LibraryContextValue {
  tracks: Track[];
  loading: boolean;
  error: string | null;
  refresh: () => void;
  removeTrack: (urn: string) => void;
  uploads: UploadItem[];
  isUploading: boolean;
  addFiles: (files: File[]) => void;
  dismissUpload: (id: string) => void;
  clearFinished: () => void;
}

const LibraryContext = createContext<LibraryContextValue | null>(null);

// A freshly completed upload isn't in the metadata read-model immediately — the
// metadata consumer has to process the event first. Re-poll a few times so the
// new track pops into the library without the user hitting refresh.
const POST_UPLOAD_REFRESH_DELAYS = [1200, 3500, 7000];

let uploadSeq = 0;
function nextId(): string {
  uploadSeq += 1;
  return `up-${Date.now().toString(36)}-${uploadSeq}`;
}

export function LibraryProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const username = user?.username ?? "";

  const [tracks, setTracks] = useState<Track[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploads, setUploads] = useState<UploadItem[]>([]);

  const reqId = useRef(0);
  const timers = useRef<number[]>([]);
  // URNs deleted locally whose removal hasn't yet propagated to the metadata
  // read-model. We hide them from every refetch until the server confirms
  // they're gone, so an in-flight poll can't briefly resurrect a deleted track.
  const pendingDeletions = useRef<Set<string>>(new Set());

  const doRefresh = useCallback(async () => {
    const id = ++reqId.current;
    setLoading(true);
    try {
      const { tracks: fetched } = await fetchTracks({ limit: 100 });
      if (id !== reqId.current) return;
      const pending = pendingDeletions.current;
      // Stop tracking any pending deletion the server has already dropped.
      for (const urn of pending) {
        if (!fetched.some((t) => t.urn === urn)) pending.delete(urn);
      }
      setTracks(pending.size ? fetched.filter((t) => !pending.has(t.urn)) : fetched);
      setError(null);
    } catch (err) {
      if (id !== reqId.current) return;
      setError(err instanceof ApiError ? err.message : "Failed to load library");
    } finally {
      if (id === reqId.current) setLoading(false);
    }
  }, []);

  const refresh = useCallback(() => void doRefresh(), [doRefresh]);

  // Delete a track: optimistically drop it, ask management to delete, then
  // reconcile. The metadata row/cover are removed asynchronously (outbox →
  // consumer), so mark it pending (hidden from refetches until the read-model
  // catches up) and re-poll a couple of times.
  const removeTrack = useCallback(
    async (urn: string) => {
      pendingDeletions.current.add(urn);
      setTracks((cur) => cur.filter((t) => t.urn !== urn));
      try {
        await deleteUpload(urn);
      } catch (err) {
        // Deletion failed (e.g. 403 not owner, 409 not ready): stop hiding it
        // and restore the true state from the server.
        pendingDeletions.current.delete(urn);
        setError(err instanceof ApiError ? err.message : "Failed to delete track");
        void doRefresh();
        return;
      }
      timers.current.push(window.setTimeout(() => void doRefresh(), 1500));
      timers.current.push(window.setTimeout(() => void doRefresh(), 4000));
    },
    [doRefresh],
  );

  // Initial load and reload when the signed-in user changes.
  useEffect(() => {
    if (username) void doRefresh();
    else setTracks([]);
  }, [username, doRefresh]);

  // Clear any pending post-upload polls on unmount.
  useEffect(() => () => timers.current.forEach((t) => clearTimeout(t)), []);

  const scheduleRefresh = useCallback(() => {
    for (const delay of POST_UPLOAD_REFRESH_DELAYS) {
      timers.current.push(window.setTimeout(() => void doRefresh(), delay));
    }
  }, [doRefresh]);

  const patchUpload = useCallback((id: string, patch: Partial<UploadItem>) => {
    setUploads((prev) => prev.map((u) => (u.id === id ? { ...u, ...patch } : u)));
  }, []);

  const setPhase = useCallback(
    (id: string, phase: UploadPhase, extra: Partial<UploadItem> = {}) => {
      patchUpload(id, { phase, ...extra });
    },
    [patchUpload],
  );

  const runUpload = useCallback(
    async (id: string, file: File) => {
      try {
        setPhase(id, "creating");
        const reserved = await createUpload(file);

        setPhase(id, "uploading", { progress: 0 });
        await putToPresigned(reserved.presignedUrl, file, reserved.contentType, (percent) =>
          patchUpload(id, { progress: percent }),
        );

        setPhase(id, "completing", { progress: 100 });
        await completeUpload(reserved.urn);

        setPhase(id, "done", { urn: reserved.urn });
        // Track metadata is produced asynchronously; poll the read-model.
        scheduleRefresh();
      } catch (err) {
        const message = err instanceof ApiError ? err.message : "Failed to upload file";
        setPhase(id, "error", { error: message });
      }
    },
    [patchUpload, setPhase, scheduleRefresh],
  );

  const addFiles = useCallback(
    (files: File[]) => {
      for (const file of files) {
        const id = nextId();
        if (!isAudioFile(file)) {
          setUploads((prev) => [
            {
              id,
              filename: file.name,
              size: file.size,
              contentType: file.type || "",
              phase: "error",
              progress: 0,
              error: "Not an audio file",
            },
            ...prev,
          ]);
          continue;
        }
        setUploads((prev) => [
          {
            id,
            filename: file.name,
            size: file.size,
            contentType: resolveContentType(file),
            phase: "queued",
            progress: 0,
          },
          ...prev,
        ]);
        void runUpload(id, file);
      }
    },
    [runUpload],
  );

  const dismissUpload = useCallback((id: string) => {
    setUploads((prev) => prev.filter((u) => u.id !== id));
  }, []);

  const clearFinished = useCallback(() => {
    setUploads((prev) => prev.filter((u) => u.phase !== "done" && u.phase !== "error"));
  }, []);

  const isUploading = uploads.some((u) => u.phase !== "done" && u.phase !== "error");

  const value = useMemo<LibraryContextValue>(
    () => ({
      tracks,
      loading,
      error,
      refresh,
      removeTrack,
      uploads,
      isUploading,
      addFiles,
      dismissUpload,
      clearFinished,
    }),
    [tracks, loading, error, refresh, removeTrack, uploads, isUploading, addFiles, dismissUpload, clearFinished],
  );

  return <LibraryContext value={value}>{children}</LibraryContext>;
}

export function useLibrary(): LibraryContextValue {
  const ctx = useContext(LibraryContext);
  if (!ctx) throw new Error("useLibrary must be used within LibraryProvider");
  return ctx;
}
