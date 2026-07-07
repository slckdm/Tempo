import { useLibrary } from "../context/LibraryContext";
import { AlertIcon, CloseIcon } from "./Icons";

/** Transient status message for mutation failures (favorites/playlists). */
export function Toast() {
  const { toast, dismissToast } = useLibrary();
  if (!toast) return null;
  return (
    <div className="toast" role="status">
      <AlertIcon size={16} />
      <span>{toast}</span>
      <button className="toast-close" onClick={dismissToast} aria-label="Dismiss">
        <CloseIcon size={14} />
      </button>
    </div>
  );
}
