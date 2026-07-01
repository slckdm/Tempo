import { useEffect, useState } from "react";
import { createPortal } from "react-dom";

import { fetchTrackMetadata, type TrackDetail } from "../api/metadata";
import { formatBytes, formatTag, formatTime } from "../lib/format";
import { useCover } from "../lib/useCover";
import type { Track } from "../types";
import { Cover } from "./Cover";
import { CloseIcon } from "./Icons";

/** Full "Month D, YYYY" date, or an em dash for an unparseable timestamp. */
function formatFullDate(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "—";
  return date.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
}

/**
 * Expanded "now playing" card: large artwork plus the track's full metadata,
 * fetched fresh from the metadata service. Opened by clicking the current track
 * in the player bar. Rendered through a portal so it overlays the whole app
 * (the player's backdrop-filter would otherwise trap a fixed child).
 */
export function TrackModal({ track, onClose }: { track: Track; onClose: () => void }) {
  const coverUrl = useCover(track);
  const [detail, setDetail] = useState<TrackDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Close on Escape for keyboard users.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  // Load the authoritative record whenever the track changes.
  useEffect(() => {
    let active = true;
    setDetail(null);
    setError(null);
    fetchTrackMetadata(track.urn)
      .then((d) => {
        if (active) setDetail(d);
      })
      .catch(() => {
        if (active) setError("Couldn't load track details");
      });
    return () => {
      active = false;
    };
  }, [track.urn]);

  // Show what the library already knows immediately; refine once the fetch lands.
  const info = detail ?? track;
  const rows: Array<[string, string | null]> = [
    ["Album", info.album],
    ["Genre", info.genre],
    ["Year", detail?.year ?? null],
    ["Duration", info.duration ? formatTime(info.duration) : null],
    ["Format", formatTag(info)],
    ["Size", formatBytes(info.size)],
    ["Added", formatFullDate(info.createdAt)],
  ];

  return createPortal(
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-label={`${info.title} details`}
        onClick={(e) => e.stopPropagation()}
      >
        <button className="modal-close" onClick={onClose} title="Close" aria-label="Close">
          <CloseIcon size={18} />
        </button>

        <div className="modal-cover">
          <Cover track={track} className="cover modal-art" imageUrl={coverUrl} />
        </div>

        <h2 className="modal-title">{info.title}</h2>
        <div className="modal-artist">{info.artist}</div>
        {error && <div className="modal-note">{error}</div>}

        <dl className="modal-meta">
          {rows
            .filter(([, value]) => value)
            .map(([label, value]) => (
              <div className="modal-meta-row" key={label}>
                <dt>{label}</dt>
                <dd>{value}</dd>
              </div>
            ))}
        </dl>
      </div>
    </div>,
    document.body,
  );
}
