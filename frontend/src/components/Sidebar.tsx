import { useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";

import { useLibrary } from "../context/LibraryContext";
import { useMediaQuery } from "../lib/useMediaQuery";
import type { LibrarySection } from "../types";
import { ChevronDownIcon, HeartIcon, MusicIcon, PlaylistIcon, PlusIcon, TrashIcon } from "./Icons";

interface SidebarProps {
  view: LibrarySection;
  onNavigate: (view: LibrarySection) => void;
}

/** Left navigation: All music, Favorites, and the user's own playlists (with create/delete). */
export function Sidebar({ view, onNavigate }: SidebarProps) {
  const { tracks, favorites, playlists, createPlaylist, deletePlaylist } = useLibrary();
  // In the compact (stacked) layout the playlist list is collapsed behind its
  // header to save vertical space; on desktop it stays expanded.
  const isCompact = useMediaQuery("(max-width: 860px)");
  const [playlistsOpen, setPlaylistsOpen] = useState(!isCompact);
  const [creating, setCreating] = useState(false);
  const [name, setName] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setPlaylistsOpen(!isCompact);
  }, [isCompact]);

  useEffect(() => {
    if (creating) inputRef.current?.focus();
  }, [creating]);

  async function submitNew(e: FormEvent) {
    e.preventDefault();
    const created = await createPlaylist(name);
    setName("");
    setCreating(false);
    if (created) onNavigate({ kind: "playlist", id: created.id });
  }

  function startCreate() {
    setPlaylistsOpen(true);
    setCreating((c) => !c);
  }

  function onDelete(id: string, plName: string) {
    if (!window.confirm(`Delete playlist “${plName}”?`)) return;
    deletePlaylist(id);
    if (view.kind === "playlist" && view.id === id) onNavigate({ kind: "all" });
  }

  return (
    <aside className="sidebar">
      <nav className="side-nav">
        <button
          className={`side-item${view.kind === "all" ? " active" : ""}`}
          onClick={() => onNavigate({ kind: "all" })}
        >
          <MusicIcon size={18} />
          <span className="side-label">All music</span>
          <span className="side-count">{tracks.length}</span>
        </button>
        <button
          className={`side-item${view.kind === "favorites" ? " active" : ""}`}
          onClick={() => onNavigate({ kind: "favorites" })}
        >
          <HeartIcon size={18} filled={view.kind === "favorites"} />
          <span className="side-label">Favorites</span>
          <span className="side-count">{favorites.length}</span>
        </button>
      </nav>

      <div className="side-section">
        <div className="side-head">
          <button
            type="button"
            className="side-head-toggle"
            onClick={() => setPlaylistsOpen((o) => !o)}
            aria-expanded={playlistsOpen}
          >
            <ChevronDownIcon size={14} className={`side-chevron${playlistsOpen ? " open" : ""}`} />
            <span className="section-title">Playlists</span>
            {playlists.length > 0 && <span className="side-pl-total">{playlists.length}</span>}
          </button>
          <button
            className="side-add"
            onClick={startCreate}
            title="New playlist"
            aria-label="New playlist"
          >
            <PlusIcon size={16} />
          </button>
        </div>

        {playlistsOpen && (
          <>
            {creating && (
              <form className="side-new" onSubmit={submitNew}>
                <input
                  ref={inputRef}
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Playlist name"
                  maxLength={80}
                  onKeyDown={(e) => {
                    if (e.key === "Escape") {
                      setCreating(false);
                      setName("");
                    }
                  }}
                />
              </form>
            )}

            <nav className="side-playlists">
              {playlists.length === 0 && !creating && (
                <div className="side-empty">No playlists yet</div>
              )}
              {playlists.map((p) => {
                const active = view.kind === "playlist" && view.id === p.id;
                return (
                  <div key={p.id} className={`side-pl${active ? " active" : ""}`}>
                    <button
                      className="side-pl-btn"
                      onClick={() => onNavigate({ kind: "playlist", id: p.id })}
                    >
                      <PlaylistIcon size={17} />
                      <span className="side-label">{p.name}</span>
                      <span className="side-count">{p.tracksCount}</span>
                    </button>
                    <button
                      className="side-pl-del"
                      onClick={() => onDelete(p.id, p.name)}
                      title="Delete playlist"
                      aria-label={`Delete playlist ${p.name}`}
                    >
                      <TrashIcon size={15} />
                    </button>
                  </div>
                );
              })}
            </nav>
          </>
        )}
      </div>
    </aside>
  );
}
