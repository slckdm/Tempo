/**
 * A processed track, sourced from the metadata service (`GET /metadata`).
 * Only tracks whose processing completed appear there.
 */
export interface Track {
  /** Backend URN, e.g. `urn:mng.upload:<uuid>` — used as the streaming id. */
  urn: string;
  /** Original filename as uploaded; null when the read-model omits it. */
  filename: string | null;
  /** Display title — metadata tag if present, otherwise parsed from filename. */
  title: string;
  /** Display artist — metadata tag if present, otherwise parsed from filename. */
  artist: string;
  album: string | null;
  genre: string | null;
  /** Duration in seconds, if the metadata service extracted it. */
  duration: number | null;
  contentType: string | null;
  size: number;
  /** Whether the metadata service has cover art for this track. */
  hasCover: boolean;
  /** ISO timestamp from the metadata record (original upload time). */
  createdAt: string;
  /** Keycloak `sub` of the uploader — only the owner may delete the track. */
  userId: string;
}

/** A user's playlist, sourced from the library service (`GET /library/playlists`). */
export interface Playlist {
  id: string;
  name: string;
  /** Number of tracks in the playlist (from the read-model). */
  tracksCount: number;
}

/** A favorited track, sourced from the library service (`GET /library/favorites`). */
export interface Favorite {
  /** The favorite record's id — needed to remove it (`DELETE /favorites/{id}`). */
  id: string;
  /** The favorited track's URN. */
  trackId: string;
}

/** Which library section is currently shown in the main view. */
export type LibrarySection =
  | { kind: "all" }
  | { kind: "favorites" }
  | { kind: "playlist"; id: string };

/** Authenticated user, decoded from the Keycloak token. */
export interface AuthUser {
  /** Keycloak `sub` — matched against a track's `userId` to gate deletion. */
  id: string;
  username: string;
  name: string;
  email?: string;
}

/** Raw Keycloak token-endpoint response (subset we use). */
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  refresh_expires_in: number;
  token_type: string;
}

export type UploadPhase =
  | "queued"
  | "creating"
  | "uploading"
  | "completing"
  | "done"
  | "error";

/** An in-flight (or just-finished) upload, shown in the upload queue. */
export interface UploadItem {
  id: string;
  filename: string;
  size: number;
  contentType: string;
  phase: UploadPhase;
  /** 0–100, meaningful during the "uploading" phase. */
  progress: number;
  error?: string;
  urn?: string;
}
