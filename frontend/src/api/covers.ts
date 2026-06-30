// Shared cover-art cache. Both the library list and the player render the same
// artwork, and many rows may want a cover at once, so we fetch each track's cover
// at most once and keep the object URL for the app's lifetime (covers are small —
// unlike the audio blobs, there's no point revoking and re-downloading them).

import { fetchCoverObjectUrl } from "./stream";

const pending = new Map<string, Promise<string | null>>();
const resolved = new Map<string, string | null>();

/** Synchronously read an already-loaded cover URL; `undefined` if not loaded yet. */
export function peekCover(urn: string): string | null | undefined {
  return resolved.get(urn);
}

/** Fetch (once) a track's cover art as an object URL, cached for the session. */
export function loadCover(urn: string): Promise<string | null> {
  if (resolved.has(urn)) return Promise.resolve(resolved.get(urn) ?? null);
  let inflight = pending.get(urn);
  if (!inflight) {
    inflight = fetchCoverObjectUrl(urn).then((url) => {
      resolved.set(urn, url);
      pending.delete(urn);
      return url;
    });
    pending.set(urn, inflight);
  }
  return inflight;
}
