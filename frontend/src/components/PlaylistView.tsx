import { useEffect, useMemo } from "react";

import { useLibrary } from "../context/LibraryContext";
import type { LibrarySection, Track } from "../types";
import { PlaylistIcon, TrashIcon } from "./Icons";
import { TrackListView } from "./TrackListView";

interface PlaylistViewProps {
  id: string;
  onNavigate: (view: LibrarySection) => void;
}

export function PlaylistView({ id, onNavigate }: PlaylistViewProps) {
  const {
    tracks,
    playlists,
    playlistTracks,
    ensurePlaylistTracks,
    reloadPlaylistTracks,
    deletePlaylist,
  } = useLibrary();

  useEffect(() => {
    ensurePlaylistTracks(id);
  }, [id, ensurePlaylistTracks]);

  const playlist = playlists.find((p) => p.id === id);
  const urns = playlistTracks[id];

  const trackByUrn = useMemo(() => new Map(tracks.map((t) => [t.urn, t] as const)), [tracks]);
  const playlistTrackList = useMemo<Track[]>(
    () => (urns ?? []).map((u) => trackByUrn.get(u)).filter((t): t is Track => Boolean(t)),
    [urns, trackByUrn],
  );

  function onDelete() {
    if (!playlist) return;
    if (!window.confirm(`Delete playlist “${playlist.name}”?`)) return;
    deletePlaylist(id);
    onNavigate({ kind: "all" });
  }

  if (!playlist) {
    return (
      <div className="empty">
        <div className="empty-icon">
          <PlaylistIcon size={28} />
        </div>
        <h3>Playlist not found</h3>
        <p>It may have been deleted.</p>
      </div>
    );
  }

  return (
    <TrackListView
      title={playlist.name}
      tracks={playlistTrackList}
      view={{ kind: "playlist", id }}
      loading={urns === undefined}
      onRefresh={() => reloadPlaylistTracks(id)}
      titleExtra={
        <button
          className="title-del"
          onClick={onDelete}
          title="Delete playlist"
          aria-label="Delete playlist"
        >
          <TrashIcon size={16} />
        </button>
      }
      emptyState={<EmptyPlaylist />}
    />
  );
}

function EmptyPlaylist() {
  return (
    <div className="empty">
      <div className="empty-icon">
        <PlaylistIcon size={28} />
      </div>
      <h3>This playlist is empty</h3>
      <p>Add tracks from any section using the “+” button on a track.</p>
    </div>
  );
}
