import { useState } from "react";

import type { LibrarySection } from "../types";
import { AllMusicView } from "./AllMusicView";
import { FavoritesView } from "./FavoritesView";
import { PlaylistView } from "./PlaylistView";
import { Sidebar } from "./Sidebar";
import { Toast } from "./Toast";

/**
 * The library workspace: a left sidebar (All music / Favorites / playlists) and
 * the section-specific content. Which section is shown is local UI state.
 */
export function LibraryView() {
  const [view, setView] = useState<LibrarySection>({ kind: "all" });
  return (
    <div className="workspace">
      <Sidebar view={view} onNavigate={setView} />
      <div className="workspace-main">
        <MainView view={view} onNavigate={setView} />
      </div>
      <Toast />
    </div>
  );
}

function MainView({
  view,
  onNavigate,
}: {
  view: LibrarySection;
  onNavigate: (view: LibrarySection) => void;
}) {
  switch (view.kind) {
    case "all":
      return <AllMusicView />;
    case "favorites":
      return <FavoritesView />;
    case "playlist":
      return <PlaylistView key={view.id} id={view.id} onNavigate={onNavigate} />;
  }
}
