import type { MouseEvent } from "react";

import { useAuth } from "../context/AuthContext";
import { useLibrary } from "../context/LibraryContext";
import { usePlayer } from "../context/PlayerContext";
import { formatAddedAt, formatBytes, formatTag, formatTime } from "../lib/format";
import { useCover } from "../lib/useCover";
import type { LibrarySection, Track } from "../types";
import { AddToPlaylistMenu } from "./AddToPlaylistMenu";
import { Cover } from "./Cover";
import { CloseIcon, HeartIcon, PlayIcon, TrashIcon } from "./Icons";

interface TrackRowProps {
  track: Track;
  index: number;
  /** The visible, sorted list — becomes the playback queue for next/prev. */
  queue: Track[];
  /** Which section this row lives in; decides the extra (non-favorite) action. */
  view: LibrarySection;
}

export function TrackRow({ track, index, queue, view }: TrackRowProps) {
  const { current, isPlaying, playTrack } = usePlayer();
  const { removeTrack, isFavorite, toggleFavorite, removeTrackFromPlaylist } = useLibrary();
  const { user } = useAuth();
  const coverUrl = useCover(track);
  const isCurrent = current?.urn === track.urn;
  const playingThis = isCurrent && isPlaying;
  const favorited = isFavorite(track.urn);
  const canDelete = user?.id === track.userId;

  const handleFavorite = (e: MouseEvent) => {
    e.stopPropagation();
    toggleFavorite(track.urn);
  };

  const handleDelete = (e: MouseEvent) => {
    e.stopPropagation();
    if (window.confirm(`Delete “${track.title}”? This can't be undone.`)) removeTrack(track.urn);
  };

  const handleRemoveFromPlaylist = (e: MouseEvent) => {
    e.stopPropagation();
    if (view.kind === "playlist") removeTrackFromPlaylist(view.id, track.urn);
  };

  return (
    <div className={`track${isCurrent ? " active" : ""}`} onClick={() => playTrack(track, queue)}>
      <div className="track-index">
        {playingThis ? (
          <div className="now-bars">
            <span />
            <span />
            <span />
          </div>
        ) : (
          <>
            <span className="idx">{index}</span>
            <span className="hover-play">
              <PlayIcon size={16} />
            </span>
          </>
        )}
      </div>

      <div className="track-main">
        <Cover track={track} imageUrl={coverUrl} />
        <div className="track-text">
          <div className="track-title">{track.title}</div>
          <div className="track-artist">
            {track.artist} · {formatTag(track)}
          </div>
        </div>
      </div>

      <span className="col-duration">{track.duration ? formatTime(track.duration) : "—"}</span>
      <span className="col-added">{formatAddedAt(track.createdAt)}</span>
      <span className="col-size">{formatBytes(track.size)}</span>

      <div className="track-actions">
        <button
          type="button"
          className={`track-fav${favorited ? " on" : ""}`}
          title={favorited ? "Remove from favorites" : "Add to favorites"}
          aria-label={favorited ? `Unfavorite ${track.title}` : `Favorite ${track.title}`}
          aria-pressed={favorited}
          onClick={handleFavorite}
        >
          <HeartIcon size={16} filled={favorited} />
        </button>

        <AddToPlaylistMenu track={track} />

        {view.kind === "playlist" && (
          <button
            type="button"
            className="track-remove"
            title="Remove from playlist"
            aria-label={`Remove ${track.title} from playlist`}
            onClick={handleRemoveFromPlaylist}
          >
            <CloseIcon size={16} />
          </button>
        )}

        {view.kind === "all" && canDelete && (
          <button
            type="button"
            className="track-del"
            title="Delete track"
            aria-label={`Delete ${track.title}`}
            onClick={handleDelete}
          >
            <TrashIcon size={16} />
          </button>
        )}
      </div>
    </div>
  );
}
