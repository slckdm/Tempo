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
}

/** Authenticated user, decoded from the Keycloak token. */
export interface AuthUser {
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
