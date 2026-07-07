import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";
import type { ReactNode } from "react";

import { ApiError } from "../api/client";
import * as libraryApi from "../api/library";
import { fetchTracks } from "../api/metadata";
import { completeUpload, createUpload, deleteUpload, putToPresigned } from "../api/uploads";
import { isAudioFile, resolveContentType } from "../lib/audioFiles";
import type { Favorite, Playlist, Track, UploadItem, UploadPhase } from "../types";
import { useAuth } from "./AuthContext";

interface LibraryContextValue {
  tracks: Track[];
  loading: boolean;
  error: string | null;
  refresh: () => void;
  removeTrack: (urn: string) => void;

  // Favorites
  favorites: Favorite[];
  isFavorite: (urn: string) => boolean;
  toggleFavorite: (urn: string) => void;
  refreshFavorites: () => void;

  // Playlists
  playlists: Playlist[];
  /** Cache of playlist id → its track URNs; a key is present only once loaded. */
  playlistTracks: Record<string, string[]>;
  ensurePlaylistTracks: (id: string) => void;
  reloadPlaylistTracks: (id: string) => void;
  createPlaylist: (name: string) => Promise<Playlist | null>;
  deletePlaylist: (id: string) => void;
  addTrackToPlaylist: (id: string, urn: string) => void;
  removeTrackFromPlaylist: (id: string, urn: string) => void;
  refreshPlaylists: () => void;

  // Transient status message (mutation failures), auto-dismissed.
  toast: string | null;
  dismissToast: () => void;

  // Uploads
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

  const [favorites, setFavorites] = useState<Favorite[]>([]);
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  const [playlistTracks, setPlaylistTracks] = useState<Record<string, string[]>>({});
  const [toast, setToast] = useState<string | null>(null);

  const reqId = useRef(0);
  const timers = useRef<number[]>([]);
  // URNs deleted locally whose removal hasn't yet propagated to the metadata
  // read-model. We hide them from every refetch until the server confirms
  // they're gone, so an in-flight poll can't briefly resurrect a deleted track.
  const pendingDeletions = useRef<Set<string>>(new Set());

  // Latest-value mirrors so the stable mutation callbacks below never read stale
  // state, and an in-flight `ensurePlaylistTracks` guard.
  const favoritesRef = useRef<Favorite[]>(favorites);
  const playlistsRef = useRef<Playlist[]>(playlists);
  const playlistTracksRef = useRef<Record<string, string[]>>(playlistTracks);
  const loadingPlaylistTracks = useRef<Set<string>>(new Set());
  const toastTimer = useRef<number | null>(null);

  useEffect(() => void (favoritesRef.current = favorites), [favorites]);
  useEffect(() => void (playlistsRef.current = playlists), [playlists]);
  useEffect(() => void (playlistTracksRef.current = playlistTracks), [playlistTracks]);

  const showToast = useCallback((message: string) => {
    setToast(message);
    if (toastTimer.current) clearTimeout(toastTimer.current);
    toastTimer.current = window.setTimeout(() => setToast(null), 3200);
  }, []);

  const dismissToast = useCallback(() => {
    if (toastTimer.current) clearTimeout(toastTimer.current);
    setToast(null);
  }, []);

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

  // ------------------------------- Favorites -------------------------------

  const favoriteUrns = useMemo(() => new Set(favorites.map((f) => f.trackId)), [favorites]);
  const isFavorite = useCallback((urn: string) => favoriteUrns.has(urn), [favoriteUrns]);

  const refreshFavorites = useCallback(async () => {
    try {
      setFavorites(await libraryApi.fetchFavorites());
    } catch {
      /* non-fatal: keep the last known favorites */
    }
  }, []);

  const toggleFavorite = useCallback(
    async (urn: string) => {
      const existing = favoritesRef.current.find((f) => f.trackId === urn);
      if (existing) {
        setFavorites((cur) => cur.filter((f) => f.trackId !== urn)); // optimistic
        try {
          await libraryApi.removeFavorite(existing.id);
        } catch {
          showToast("Couldn't remove from favorites");
          void refreshFavorites();
        }
      } else {
        // Optimistically fill the heart with a placeholder id, then re-fetch to
        // learn the real favorite id (the add response doesn't return it).
        setFavorites((cur) => [...cur, { id: `pending:${urn}`, trackId: urn }]);
        try {
          await libraryApi.addFavorite(urn);
          await refreshFavorites();
        } catch {
          setFavorites((cur) => cur.filter((f) => f.trackId !== urn));
          showToast("Couldn't add to favorites");
        }
      }
    },
    [showToast, refreshFavorites],
  );

  // ------------------------------- Playlists -------------------------------

  const refreshPlaylists = useCallback(async () => {
    try {
      setPlaylists(await libraryApi.fetchPlaylists());
    } catch {
      /* non-fatal: keep the last known playlists */
    }
  }, []);

  const ensurePlaylistTracks = useCallback(async (id: string) => {
    if (playlistTracksRef.current[id] !== undefined) return;
    if (loadingPlaylistTracks.current.has(id)) return;
    loadingPlaylistTracks.current.add(id);
    try {
      const urns = await libraryApi.fetchPlaylistTracks(id);
      setPlaylistTracks((cur) => ({ ...cur, [id]: urns }));
    } catch {
      /* leave unloaded; the view falls back to an empty/loading state */
    } finally {
      loadingPlaylistTracks.current.delete(id);
    }
  }, []);

  const reloadPlaylistTracks = useCallback(
    async (id: string) => {
      try {
        const urns = await libraryApi.fetchPlaylistTracks(id);
        setPlaylistTracks((cur) => ({ ...cur, [id]: urns }));
        setPlaylists((cur) => cur.map((p) => (p.id === id ? { ...p, tracksCount: urns.length } : p)));
      } catch {
        showToast("Couldn't refresh playlist");
      }
    },
    [showToast],
  );

  const createPlaylist = useCallback(
    async (name: string): Promise<Playlist | null> => {
      const trimmed = name.trim();
      if (!trimmed) return null;
      try {
        const created = await libraryApi.createPlaylist(trimmed);
        setPlaylists((cur) => [...cur, created]);
        setPlaylistTracks((cur) => ({ ...cur, [created.id]: [] }));
        return created;
      } catch {
        showToast("Couldn't create playlist");
        return null;
      }
    },
    [showToast],
  );

  const deletePlaylist = useCallback(
    async (id: string) => {
      const prev = playlistsRef.current;
      setPlaylists((cur) => cur.filter((p) => p.id !== id));
      setPlaylistTracks((cur) => {
        const next = { ...cur };
        delete next[id];
        return next;
      });
      try {
        await libraryApi.deletePlaylist(id);
      } catch {
        setPlaylists(prev);
        showToast("Couldn't delete playlist");
        void refreshPlaylists();
      }
    },
    [showToast, refreshPlaylists],
  );

  const bumpCount = (id: string, delta: number) =>
    setPlaylists((cur) =>
      cur.map((p) => (p.id === id ? { ...p, tracksCount: Math.max(0, p.tracksCount + delta) } : p)),
    );

  const addTrackToPlaylist = useCallback(
    async (id: string, urn: string) => {
      const known = playlistTracksRef.current[id];
      if (known?.includes(urn)) return; // already present — don't create a duplicate row
      if (known) {
        setPlaylistTracks((cur) => ({ ...cur, [id]: [...(cur[id] ?? []), urn] }));
        bumpCount(id, 1);
        try {
          await libraryApi.addTrackToPlaylist(id, urn);
        } catch {
          setPlaylistTracks((cur) => ({ ...cur, [id]: (cur[id] ?? []).filter((u) => u !== urn) }));
          bumpCount(id, -1);
          showToast("Couldn't add to playlist");
        }
      } else {
        // Membership unknown — write, then load the authoritative list.
        try {
          await libraryApi.addTrackToPlaylist(id, urn);
          const urns = await libraryApi.fetchPlaylistTracks(id);
          setPlaylistTracks((cur) => ({ ...cur, [id]: urns }));
          setPlaylists((cur) =>
            cur.map((p) => (p.id === id ? { ...p, tracksCount: urns.length } : p)),
          );
        } catch {
          showToast("Couldn't add to playlist");
        }
      }
    },
    [showToast],
  );

  const removeTrackFromPlaylist = useCallback(
    async (id: string, urn: string) => {
      const known = playlistTracksRef.current[id];
      setPlaylistTracks((cur) => ({ ...cur, [id]: (cur[id] ?? []).filter((u) => u !== urn) }));
      bumpCount(id, -1);
      try {
        await libraryApi.removeTrackFromPlaylist(id, urn);
      } catch {
        if (known) setPlaylistTracks((cur) => ({ ...cur, [id]: known }));
        bumpCount(id, 1);
        showToast("Couldn't remove from playlist");
      }
    },
    [showToast],
  );

  // Initial load and reload when the signed-in user changes.
  useEffect(() => {
    if (username) {
      void doRefresh();
      void refreshFavorites();
      void refreshPlaylists();
    } else {
      setTracks([]);
      setFavorites([]);
      setPlaylists([]);
      setPlaylistTracks({});
    }
  }, [username, doRefresh, refreshFavorites, refreshPlaylists]);

  // Clear any pending post-upload polls / toast timer on unmount.
  useEffect(() => () => timers.current.forEach((t) => clearTimeout(t)), []);
  useEffect(() => () => void (toastTimer.current && clearTimeout(toastTimer.current)), []);

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
      favorites,
      isFavorite,
      toggleFavorite,
      refreshFavorites,
      playlists,
      playlistTracks,
      ensurePlaylistTracks,
      reloadPlaylistTracks,
      createPlaylist,
      deletePlaylist,
      addTrackToPlaylist,
      removeTrackFromPlaylist,
      refreshPlaylists,
      toast,
      dismissToast,
      uploads,
      isUploading,
      addFiles,
      dismissUpload,
      clearFinished,
    }),
    [
      tracks, loading, error, refresh, removeTrack, favorites, isFavorite, toggleFavorite,
      refreshFavorites, playlists, playlistTracks, ensurePlaylistTracks, reloadPlaylistTracks,
      createPlaylist, deletePlaylist, addTrackToPlaylist, removeTrackFromPlaylist, refreshPlaylists,
      toast, dismissToast, uploads, isUploading, addFiles, dismissUpload, clearFinished,
    ],
  );

  return <LibraryContext value={value}>{children}</LibraryContext>;
}

export function useLibrary(): LibraryContextValue {
  const ctx = useContext(LibraryContext);
  if (!ctx) throw new Error("useLibrary must be used within LibraryProvider");
  return ctx;
}
