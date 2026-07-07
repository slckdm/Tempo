import { useMemo, useState } from "react";
import type { ReactNode } from "react";

import { formatTag } from "../lib/format";
import type { LibrarySection, Track } from "../types";
import { AlertIcon, RefreshIcon, SearchIcon, SpinnerIcon } from "./Icons";
import { TrackRow } from "./TrackRow";

type SortKey = "recent" | "title" | "artist" | "duration" | "size";

const SORTERS: Record<SortKey, (a: Track, b: Track) => number> = {
  recent: (a, b) => b.createdAt.localeCompare(a.createdAt),
  title: (a, b) => a.title.localeCompare(b.title, "en"),
  artist: (a, b) => a.artist.localeCompare(b.artist, "en"),
  duration: (a, b) => (b.duration ?? 0) - (a.duration ?? 0),
  size: (a, b) => b.size - a.size,
};

interface TrackListViewProps {
  title: string;
  tracks: Track[];
  view: LibrarySection;
  loading?: boolean;
  error?: string | null;
  onRetry?: () => void;
  onRefresh?: () => void;
  refreshing?: boolean;
  /** Controls rendered at the right of the header, e.g. the Upload button. */
  headerActions?: ReactNode;
  /** Rendered inside the title, e.g. a delete-playlist button. */
  titleExtra?: ReactNode;
  /** Shown when there are no tracks at all (distinct from "no search results"). */
  emptyState: ReactNode;
}

/**
 * Reusable track list with search / format-filter / sort controls, shared by the
 * All music, Favorites and per-playlist views. The `view` prop is threaded to
 * each row so it renders the section-appropriate actions.
 */
export function TrackListView({
  title,
  tracks,
  view,
  loading = false,
  error = null,
  onRetry,
  onRefresh,
  refreshing = false,
  headerActions,
  titleExtra,
  emptyState,
}: TrackListViewProps) {
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState<SortKey>("recent");
  const [format, setFormat] = useState("all");

  const formats = useMemo(() => {
    const set = new Set(tracks.map(formatTag));
    return Array.from(set).sort();
  }, [tracks]);

  // Ignore a format filter that no longer matches anything in this list.
  const activeFormat = format !== "all" && !formats.includes(format) ? "all" : format;

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase();
    return tracks
      .filter((t) => (activeFormat === "all" ? true : formatTag(t) === activeFormat))
      .filter((t) =>
        q === ""
          ? true
          : t.title.toLowerCase().includes(q) ||
            t.artist.toLowerCase().includes(q) ||
            (t.album?.toLowerCase().includes(q) ?? false) ||
            (t.filename?.toLowerCase().includes(q) ?? false),
      )
      .sort(SORTERS[sort]);
  }, [tracks, query, sort, activeFormat]);

  return (
    <section>
      <div className="library-head">
        <h1 className="library-title">
          {title}
          <span className="library-count">{tracks.length}</span>
          {titleExtra}
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
              value={activeFormat}
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
          {onRefresh && (
            <button
              className="refresh-btn"
              onClick={onRefresh}
              disabled={refreshing}
              title="Refresh"
              aria-label="Refresh"
            >
              {refreshing ? <SpinnerIcon size={18} /> : <RefreshIcon size={18} />}
            </button>
          )}
          {headerActions}
        </div>
      </div>

      {error && tracks.length === 0 ? (
        <ListError message={error} onRetry={onRetry} />
      ) : loading && tracks.length === 0 ? (
        <ListLoading />
      ) : tracks.length === 0 ? (
        emptyState
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
            <span className="col-actions" aria-hidden="true" />
          </div>
          <div className="tracklist">
            {visible.map((track, i) => (
              <TrackRow key={track.urn} track={track} index={i + 1} queue={visible} view={view} />
            ))}
          </div>
        </>
      )}
    </section>
  );
}

function ListLoading() {
  return (
    <div className="empty">
      <div className="empty-icon">
        <SpinnerIcon size={28} />
      </div>
      <h3>Loading…</h3>
      <p>Fetching the track list.</p>
    </div>
  );
}

function ListError({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="empty">
      <div className="empty-icon">
        <AlertIcon size={28} />
      </div>
      <h3>Something went wrong</h3>
      <p>{message}</p>
      {onRetry && (
        <button className="retry" onClick={onRetry}>
          Retry
        </button>
      )}
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
      <p>Try a different search or reset the filters.</p>
    </div>
  );
}
