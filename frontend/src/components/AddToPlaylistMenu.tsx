import { useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";

import { useLibrary } from "../context/LibraryContext";
import type { Track } from "../types";
import { CheckIcon, PlusIcon } from "./Icons";

/**
 * Per-track popover for adding/removing the track to/from the user's playlists.
 * Each playlist row is a checkbox toggle (add if absent, remove if present), and
 * a "New playlist" affordance creates a playlist and adds the track in one step.
 * Membership is read from the shared cache, loaded when the menu opens.
 */
export function AddToPlaylistMenu({ track }: { track: Track }) {
  const {
    playlists,
    playlistTracks,
    ensurePlaylistTracks,
    addTrackToPlaylist,
    removeTrackFromPlaylist,
    createPlaylist,
  } = useLibrary();
  const rootRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [open, setOpen] = useState(false);
  const [creating, setCreating] = useState(false);
  const [name, setName] = useState("");

  // Load membership for every playlist when the menu opens, to show checkmarks.
  useEffect(() => {
    if (open) playlists.forEach((p) => ensurePlaylistTracks(p.id));
  }, [open, playlists, ensurePlaylistTracks]);

  // Close on outside click / Escape.
  useEffect(() => {
    if (!open) return;
    function onPointerDown(e: MouseEvent) {
      if (rootRef.current && !rootRef.current.contains(e.target as Node)) setOpen(false);
    }
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    document.addEventListener("mousedown", onPointerDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onPointerDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  useEffect(() => {
    if (creating) inputRef.current?.focus();
  }, [creating]);

  function toggleMembership(playlistId: string) {
    if ((playlistTracks[playlistId] ?? []).includes(track.urn)) {
      removeTrackFromPlaylist(playlistId, track.urn);
    } else {
      addTrackToPlaylist(playlistId, track.urn);
    }
  }

  async function submitNew(e: FormEvent) {
    e.preventDefault();
    const created = await createPlaylist(name);
    setName("");
    setCreating(false);
    setOpen(false);
    if (created) addTrackToPlaylist(created.id, track.urn);
  }

  return (
    <div className="add-menu" ref={rootRef}>
      <button
        type="button"
        className={`track-add${open ? " on" : ""}`}
        title="Add to playlist"
        aria-label={`Add ${track.title} to a playlist`}
        aria-haspopup="menu"
        aria-expanded={open}
        onClick={(e) => {
          e.stopPropagation();
          setOpen((o) => !o);
        }}
      >
        <PlusIcon size={16} />
      </button>

      {open && (
        <div className="add-pop" role="menu" onClick={(e) => e.stopPropagation()}>
          <div className="add-pop-title">Add to playlist</div>
          <div className="add-pop-list">
            {playlists.length === 0 && !creating && (
              <div className="add-pop-empty">No playlists yet</div>
            )}
            {playlists.map((p) => {
              const inList = (playlistTracks[p.id] ?? []).includes(track.urn);
              return (
                <button
                  key={p.id}
                  type="button"
                  className={`add-pop-item${inList ? " on" : ""}`}
                  role="menuitemcheckbox"
                  aria-checked={inList}
                  onClick={() => toggleMembership(p.id)}
                >
                  <span className="add-pop-name">{p.name}</span>
                  {inList && <CheckIcon size={15} />}
                </button>
              );
            })}
          </div>

          {creating ? (
            <form className="add-pop-new" onSubmit={submitNew}>
              <input
                ref={inputRef}
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Playlist name"
                maxLength={80}
                onKeyDown={(e) => {
                  if (e.key === "Escape") {
                    e.stopPropagation();
                    setCreating(false);
                    setName("");
                  }
                }}
              />
              <button type="submit" className="add-pop-create" disabled={!name.trim()}>
                Create
              </button>
            </form>
          ) : (
            <button type="button" className="add-pop-add" onClick={() => setCreating(true)}>
              <PlusIcon size={15} /> New playlist
            </button>
          )}
        </div>
      )}
    </div>
  );
}
