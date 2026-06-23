// The streaming service requires a bearer token, but <audio src> / <img src>
// can't send Authorization headers. So we fetch the bytes with auth and hand the
// element a blob: URL instead. Blob URLs are fully seekable, so scrubbing works;
// the trade-off is the whole track loads up front (fine for a music player).

import { config } from "../config";
import { authedFetch, ApiError } from "./client";

function streamPath(urn: string): string {
  return `${config.streamingBase}/stream/${encodeURIComponent(urn)}`;
}

/** Download a track and return an object URL. Caller must revokeObjectURL it. */
export async function fetchAudioObjectUrl(urn: string): Promise<string> {
  const res = await authedFetch(streamPath(urn));
  if (!res.ok) {
    throw new ApiError(`Failed to load track (${res.status})`, res.status);
  }
  const blob = await res.blob();
  return URL.createObjectURL(blob);
}

/**
 * Download a track's cover art and return an object URL, or null if the backend
 * has no cover for it (the cover-extraction pipeline may not be running).
 */
export async function fetchCoverObjectUrl(urn: string): Promise<string | null> {
  try {
    const res = await authedFetch(`${streamPath(urn)}/cover`);
    if (!res.ok) return null;
    const blob = await res.blob();
    if (blob.size === 0) return null;
    return URL.createObjectURL(blob);
  } catch {
    return null;
  }
}
