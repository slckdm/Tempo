// The streaming service requires a token, but <audio src> / <img src> can't send
// an Authorization header. Audio now streams natively: we hand the element the
// same-origin stream URL and the backend authenticates via the access-token
// cookie (kept in sync by auth.ts), so the browser does real HTTP Range requests
// and seeking only fetches the bytes it needs. Covers are tiny, so they still use
// the fetch-to-blob path below.

import { config } from "../config";
import { authedFetch } from "./client";
import { getAccessToken } from "./auth";

function streamPath(urn: string): string {
  return `${config.streamingBase}/stream/${encodeURIComponent(urn)}`;
}

/**
 * Resolve a track's same-origin stream URL for direct use as an <audio> src.
 * Refreshes the token first (if near expiry) so the auth cookie is fresh when
 * the element starts requesting bytes. Returns null if the session is gone.
 */
export async function resolveAudioStreamUrl(urn: string): Promise<string | null> {
  const token = await getAccessToken();
  if (!token) return null;
  return streamPath(urn);
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
