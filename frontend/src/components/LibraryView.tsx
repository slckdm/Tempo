import { useMemo, useState } from "react";

import { useLibrary } from "../context/LibraryContext";
import { usePlayer } from "../context/PlayerContext";
import { formatAddedAt, formatBytes, formatTime } from "../lib/format";
import type { Track } from "../types";
import { Cover } from "./Cover";
import { AlertIcon, MusicIcon, PlayIcon, RefreshIcon, SearchIcon, SpinnerIcon } from "./Icons";

type SortKey = "recent" | "title" | "artist" | "duration" | "size";

const SORTERS: Record<SortKey, (a: Track, b: Track) => number> = {
  recent: (a, b) => b.createdAt.localeCompare(a.createdAt),
  title: (a, b) => a.title.localeCompare(b.title, "en"),
  artist: (a, b) => a.artist.localeCompare(b.artist, "en"),
  duration: (a, b) => (b.duration ?? 0) - (a.duration ?? 0),
  size: (a, b) => b.size - a.size,
};

/** A short, uppercase format tag from a content type or filename. */
function formatTag(track: Track): string {
  const fromType = track.contentType?.split("/")[1]?.toUpperCase();
  const map: Record<string, string> = { MPEG: "MP3", "X-WAV": "WAV", "MP4": "M4A" };
  if (fromType) return map[fromType] ?? fromType;
  const ext = track.filename?.split(".").pop()?.toUpperCase();
  return ext ?? "AUDIO";
}

export function LibraryView() {
  const { tracks, loading, error, refresh } = useLibrary();
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState<SortKey>("recent");
  const [format, setFormat] = useState("all");

  const formats = useMemo(() => {
    const set = new Set(tracks.map(formatTag));
    return Array.from(set).sort();
  }, [tracks]);

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase();
    return tracks
      .filter((t) => (format === "all" ? true : formatTag(t) === format))
      .filter((t) =>
        q === ""
          ? true
          : t.title.toLowerCase().includes(q) ||
            t.artist.toLowerCase().includes(q) ||
            (t.album?.toLowerCase().includes(q) ?? false) ||
            (t.filename?.toLowerCase().includes(q) ?? false),
      )
      .sort(SORTERS[sort]);
  }, [tracks, query, sort, format]);

  return (
    <section>
      <div className="library-head">
        <h1 className="library-title">
          My music
          <span className="library-count">{tracks.length}</span>
        </h1>
        <div className="controls">
          <div className="search">
            <SearchIcon size={17} />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by title, artist…"
            />
          </div>
          {formats.length > 1 && (
            <select
              className="select"
              value={format}
              onChange={(e) => setFormat(e.target.value)}
              aria-label="Filter by format"
            >
              <option value="all">All formats</option>
              {formats.map((f) => (
                <option key={f} value={f}>
                  {f}
                </option>
              ))}
            </select>
          )}
          <select
            className="select"
            value={sort}
            onChange={(e) => setSort(e.target.value as SortKey)}
            aria-label="Sort"
          >
            <option value="recent">Recent</option>
            <option value="title">By title</option>
            <option value="artist">By artist</option>
            <option value="duration">By duration</option>
            <option value="size">By size</option>
          </select>
          <button
            className="refresh-btn"
            onClick={refresh}
            disabled={loading}
            title="Refresh library"
            aria-label="Refresh library"
          >
            {loading ? <SpinnerIcon size={18} /> : <RefreshIcon size={18} />}
          </button>
        </div>
      </div>

      {error && tracks.length === 0 ? (
        <LibraryError message={error} onRetry={refresh} />
      ) : loading && tracks.length === 0 ? (
        <LibraryLoading />
      ) : tracks.length === 0 ? (
        <EmptyLibrary />
      ) : visible.length === 0 ? (
        <NoResults />
      ) : (
        <>
          <div className="track-head">
            <span>#</span>
            <span>Title</span>
            <span className="col-duration">Time</span>
            <span className="col-added">Added</span>
            <span className="col-size">Size</span>
          </div>
          <div className="tracklist">
            {visible.map((track, i) => (
              <TrackRow key={track.urn} track={track} index={i + 1} queue={visible} />
            ))}
          </div>
        </>
      )}
    </section>
  );
}

function TrackRow({ track, index, queue }: { track: Track; index: number; queue: Track[] }) {
  const { current, isPlaying, playTrack } = usePlayer();
  const isCurrent = current?.urn === track.urn;
  const playingThis = isCurrent && isPlaying;

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
        <Cover track={track} />
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
    </div>
  );
}

function LibraryLoading() {
  return (
    <div className="empty">
      <div className="empty-icon">
        <SpinnerIcon size={28} />
      </div>
      <h3>Loading library…</h3>
      <p>Fetching the track list from the metadata service.</p>
    </div>
  );
}

function LibraryError({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div className="empty">
      <div className="empty-icon">
        <AlertIcon size={28} />
      </div>
      <h3>Failed to load library</h3>
      <p>{message}. Make sure the metadata service is running.</p>
      <button className="retry" onClick={onRetry}>
        Retry
      </button>
    </div>
  );
}

function EmptyLibrary() {
  return (
    <div className="empty">
      <div className="empty-icon">
        <MusicIcon size={30} />
      </div>
      <h3>Nothing here yet</h3>
      <p>
        Upload your first track from the panel on the left. Once its metadata is processed,
        it'll appear here and be ready to play.
      </p>
    </div>
  );
}

function NoResults() {
  return (
    <div className="empty">
      <div className="empty-icon">
        <SearchIcon size={28} />
      </div>
      <h3>Nothing found</h3>
      <p>Try a different search or reset the format filter.</p>
    </div>
  );
}
