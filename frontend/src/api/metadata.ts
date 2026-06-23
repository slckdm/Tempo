// The metadata service is the read-model for the library: it consumes upload
// events, extracts tags (title/artist/album/duration/cover) and exposes a
// filterable, paginated list of *completed* tracks via `GET /metadata`.

import { config } from "../config";
import { parseTrackName } from "../lib/format";
import type { Track } from "../types";
import { apiJson } from "./client";

/** Shape returned by the metadata service (field names are its API aliases). */
interface TrackMetadataDTO {
  urn: string;
  title: string | null;
  artist: string | null;
  album: string | null;
  genre: string | null;
  duration: number | null;
  cover_key: string | null;
  filename: string;
  content_type: string;
  size: number;
  created_at: string;
  processing_status: string;
}

interface TracksMetadataResponse {
  metadata: TrackMetadataDTO[];
  pagination: { limit: number; offset: number; total: number };
}

/** Server-side filters the metadata list endpoint understands. */
export interface MetadataQuery {
  offset?: number;
  limit?: number;
  title?: string;
  artist?: string;
  album?: string;
  genre?: string;
}

function toTrack(dto: TrackMetadataDTO): Track {
  const parsed = parseTrackName(dto.filename);
  return {
    urn: dto.urn,
    filename: dto.filename,
    title: dto.title?.trim() || parsed.title,
    artist: dto.artist?.trim() || parsed.artist,
    album: dto.album?.trim() || null,
    genre: dto.genre?.trim() || null,
    duration: typeof dto.duration === "number" ? dto.duration : null,
    contentType: dto.content_type,
    size: dto.size,
    hasCover: Boolean(dto.cover_key),
    createdAt: dto.created_at,
  };
}

export interface TracksPage {
  tracks: Track[];
  total: number;
}

/** Fetch the library page from the metadata service. */
export async function fetchTracks(query: MetadataQuery = {}): Promise<TracksPage> {
  const params = new URLSearchParams();
  params.set("offset", String(query.offset ?? 0));
  params.set("limit", String(query.limit ?? 100));
  if (query.title) params.set("title", query.title);
  if (query.artist) params.set("artist", query.artist);
  if (query.album) params.set("album", query.album);
  if (query.genre) params.set("genre", query.genre);

  const data = await apiJson<TracksMetadataResponse>(
    `${config.metadataBase}/?${params.toString()}`,
  );
  return { tracks: data.metadata.map(toTrack), total: data.pagination.total };
}
