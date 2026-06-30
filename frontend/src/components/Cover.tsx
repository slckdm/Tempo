import { coverGradient, initials } from "../lib/format";
import type { Track } from "../types";

interface CoverProps {
  track: Pick<Track, "urn" | "title" | "artist">;
  className?: string;
  /** Optional fetched cover image (object URL). Falls back to a gradient. */
  imageUrl?: string | null;
}

/**
 * Track artwork. Callers pass the fetched cover image (via `useCover`); when it's
 * absent or still loading, we render a deterministic gradient placeholder.
 */
export function Cover({ track, className = "cover", imageUrl }: CoverProps) {
  if (imageUrl) {
    return (
      <div className={className}>
        <img src={imageUrl} alt="" />
      </div>
    );
  }
  return (
    <div className={className} style={{ background: coverGradient(track.urn) }}>
      {initials(track)}
    </div>
  );
}
