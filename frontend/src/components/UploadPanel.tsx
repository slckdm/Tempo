import { useRef, useState } from "react";
import type { ChangeEvent, DragEvent } from "react";

import { useLibrary } from "../context/LibraryContext";
import { AUDIO_ACCEPT } from "../lib/audioFiles";
import { formatBytes } from "../lib/format";
import type { UploadItem, UploadPhase } from "../types";
import { AlertIcon, CheckIcon, CloseIcon, SpinnerIcon, UploadIcon } from "./Icons";

const PHASE_LABEL: Record<UploadPhase, string> = {
  queued: "Queued",
  creating: "Preparing…",
  uploading: "Uploading",
  completing: "Finishing…",
  done: "Done",
  error: "Error",
};

export function UploadPanel() {
  const { uploads, addFiles, dismissUpload, clearFinished } = useLibrary();
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  function onPick(e: ChangeEvent<HTMLInputElement>) {
    if (e.target.files) addFiles(Array.from(e.target.files));
    e.target.value = "";
  }

  function onDrop(e: DragEvent) {
    e.preventDefault();
    setDragging(false);
    if (e.dataTransfer.files?.length) addFiles(Array.from(e.dataTransfer.files));
  }

  const hasFinished = uploads.some((u) => u.phase === "done" || u.phase === "error");

  return (
    <aside className="panel upload-sticky">
      <h2 className="section-title">Upload</h2>

      <div
        className={`dropzone${dragging ? " drag" : ""}`}
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") inputRef.current?.click();
        }}
      >
        <div className="dropzone-icon">
          <UploadIcon size={24} />
        </div>
        <div>
          Drag audio here or <span className="dropzone-browse">browse files</span>
        </div>
        <div className="dropzone-hint">MP3, FLAC, WAV, M4A, OGG, OPUS…</div>
        <input
          ref={inputRef}
          type="file"
          accept={AUDIO_ACCEPT}
          multiple
          onChange={onPick}
          className="sr-only"
        />
      </div>

      {uploads.length > 0 && (
        <div className="queue">
          <div className="queue-head">
            <h2 className="section-title" style={{ margin: 0 }}>
              Queue
            </h2>
            {hasFinished && (
              <button className="link-btn" onClick={clearFinished}>
                Clear
              </button>
            )}
          </div>
          {uploads.map((u) => (
            <QueueRow key={u.id} item={u} onDismiss={() => dismissUpload(u.id)} />
          ))}
        </div>
      )}
    </aside>
  );
}

function QueueRow({ item, onDismiss }: { item: UploadItem; onDismiss: () => void }) {
  const done = item.phase === "done";
  const error = item.phase === "error";
  const active = !done && !error;
  const showBar = item.phase === "uploading" || item.phase === "completing";

  return (
    <div className="queue-item">
      <div className="queue-row">
        <span className={`queue-status ${done ? "ok" : error ? "err" : "busy"}`}>
          {done ? (
            <CheckIcon size={18} />
          ) : error ? (
            <AlertIcon size={18} />
          ) : (
            <SpinnerIcon size={18} />
          )}
        </span>
        <div className="queue-info">
          <div className="queue-name" title={item.filename}>
            {item.filename}
          </div>
          <div className={`queue-meta${error ? " err" : ""}`}>
            {error
              ? item.error
              : `${PHASE_LABEL[item.phase]} · ${formatBytes(item.size)}${
                  item.phase === "uploading" ? ` · ${item.progress}%` : ""
                }`}
          </div>
        </div>
        {!active && (
          <button className="queue-dismiss" onClick={onDismiss} aria-label="Remove from queue">
            <CloseIcon size={15} />
          </button>
        )}
      </div>
      {showBar && (
        <div className="progress">
          <span style={{ width: `${item.progress}%` }} />
        </div>
      )}
    </div>
  );
}
