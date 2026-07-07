import { useLibrary } from "../context/LibraryContext";
import { MusicIcon } from "./Icons";
import { TrackListView } from "./TrackListView";
import { UploadMenu } from "./UploadMenu";

export function AllMusicView() {
  const { tracks, loading, error, refresh } = useLibrary();
  return (
    <TrackListView
      title="All music"
      tracks={tracks}
      view={{ kind: "all" }}
      loading={loading}
      error={error}
      onRetry={refresh}
      onRefresh={refresh}
      refreshing={loading}
      headerActions={<UploadMenu />}
      emptyState={<EmptyLibrary />}
    />
  );
}

function EmptyLibrary() {
  return (
    <div className="empty">
      <div className="empty-icon">
        <MusicIcon size={30} />
      </div>
      <h3>Nothing here yet</h3>
      <p>
        Upload your first track with the Upload button above. Once its metadata is processed, it'll
        appear here and be ready to play.
      </p>
    </div>
  );
}
