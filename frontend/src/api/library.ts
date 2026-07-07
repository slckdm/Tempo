// The library service owns per-user favorites and playlists. It references
// tracks purely by their management URN (e.g. `urn:mng.upload:<uuid>`), the same
// id the metadata read-model uses, so the frontend resolves those URNs against
// the already-loaded track list. Auth is the plain session bearer: the library
// authorizes with the `tempo:etc` audience the session token already carries.

import { config } from "../config";
import type { Favorite, Playlist } from "../types";
import { apiJson } from "./client";

// ----------------------------------- Favorites -----------------------------------

interface FavoriteDTO {
  id: string;
  user_id: string;
  track_id: string;
}

interface FavoritesResponse {
  favorites: FavoriteDTO[];
}

export async function fetchFavorites(): Promise<Favorite[]> {
  const data = await apiJson<FavoritesResponse>(`${config.libraryBase}/favorites/`);
  return data.favorites.map((f) => ({ id: f.id, trackId: f.track_id }));
}

/**
 * Favorite a track. The endpoint is idempotent (favoriting twice is a no-op) but
 * its response only echoes the track_id, not the new favorite's id — callers that
 * need the id for later removal should re-fetch the favorites list.
 */
export async function addFavorite(trackId: string): Promise<void> {
  await apiJson(`${config.libraryBase}/favorites/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ track_id: trackId }),
  });
}

/** Remove a favorite by its record id (not the track URN). */
export async function removeFavorite(favoriteId: string): Promise<void> {
  await apiJson(`${config.libraryBase}/favorites/${encodeURIComponent(favoriteId)}`, {
    method: "DELETE",
  });
}

// ----------------------------------- Playlists -----------------------------------

interface PlaylistDTO {
  id: string;
  user_id: string;
  name: string;
  tracks_count: number;
}

interface PlaylistsResponse {
  playlists: PlaylistDTO[];
  total: number;
  limit: number;
  offset: number;
}

function toPlaylist(dto: PlaylistDTO): Playlist {
  return { id: dto.id, name: dto.name, tracksCount: dto.tracks_count };
}

export async function fetchPlaylists(): Promise<Playlist[]> {
  const data = await apiJson<PlaylistsResponse>(
    `${config.libraryBase}/playlists/?offset=0&limit=50`,
  );
  return data.playlists.map(toPlaylist);
}

interface CreatePlaylistResponse {
  id: string;
  user_id: string;
  name: string;
}

export async function createPlaylist(name: string): Promise<Playlist> {
  const data = await apiJson<CreatePlaylistResponse>(`${config.libraryBase}/playlists/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  return { id: data.id, name: data.name, tracksCount: 0 };
}

export async function deletePlaylist(playlistId: string): Promise<void> {
  await apiJson(`${config.libraryBase}/playlists/${encodeURIComponent(playlistId)}`, {
    method: "DELETE",
  });
}

interface TracksResponse {
  tracks: string[];
}

/** Fetch the ordered list of track URNs in a playlist. */
export async function fetchPlaylistTracks(playlistId: string): Promise<string[]> {
  const data = await apiJson<TracksResponse>(
    `${config.libraryBase}/playlists/${encodeURIComponent(playlistId)}/tracks`,
  );
  return data.tracks;
}

export async function addTrackToPlaylist(playlistId: string, trackId: string): Promise<void> {
  await apiJson(`${config.libraryBase}/playlists/${encodeURIComponent(playlistId)}/tracks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ track_id: trackId }),
  });
}

export async function removeTrackFromPlaylist(
  playlistId: string,
  trackId: string,
): Promise<void> {
  const params = new URLSearchParams({ track_id: trackId });
  await apiJson(
    `${config.libraryBase}/playlists/${encodeURIComponent(playlistId)}/tracks?${params.toString()}`,
    { method: "DELETE" },
  );
}
