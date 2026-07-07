import { useMemo } from "react";

import { useLibrary } from "../context/LibraryContext";
import type { Track } from "../types";
import { HeartIcon } from "./Icons";
import { TrackListView } from "./TrackListView";

export function FavoritesView() {
  const { tracks, favorites, isFavorite, refreshFavorites } = useLibrary();

  // Resolve favorited URNs against the loaded library; favorites whose track
  // isn't in the read-model yet (still processing) simply don't appear.
  const favoriteTracks = useMemo<Track[]>(
    () => tracks.filter((t) => isFavorite(t.urn)),
    [tracks, isFavorite],
  );

  return (
    <TrackListView
      title="Favorites"
      tracks={favoriteTracks}
      view={{ kind: "favorites" }}
      onRefresh={refreshFavorites}
      emptyState={<EmptyFavorites hasFavorites={favorites.length > 0} />}
    />
  );
}

function EmptyFavorites({ hasFavorites }: { hasFavorites: boolean }) {
  return (
    <div className="empty">
      <div className="empty-icon">
        <HeartIcon size={28} />
      </div>
      <h3>No favorites yet</h3>
      <p>
        {hasFavorites
          ? "Your favorited tracks aren't in the library view yet — they may still be processing."
          : "Tap the heart on any track to add it here."}
      </p>
    </div>
  );
}
