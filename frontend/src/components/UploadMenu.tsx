import { useEffect, useRef, useState } from "react";
import type { ChangeEvent, DragEvent } from "react";

import { useLibrary } from "../context/LibraryContext";
import { AUDIO_ACCEPT } from "../lib/audioFiles";
import { formatBytes } from "../lib/format";
import type { UploadItem, UploadPhase } from "../types";
import {
  AlertIcon,
  CheckIcon,
  ChevronDownIcon,
  CloseIcon,
  SpinnerIcon,
  UploadIcon,
} from "./Icons";

const PHASE_LABEL: Record<UploadPhase, string> = {
  queued: "Queued",
  creating: "Preparing…",
  uploading: "Uploading",
  completing: "Finishing…",
  done: "Done",
  error: "Error",
};

/**
 * Upload entry point: a button in the library controls that opens a popover with
 * the dropzone and the in-flight upload queue. Closes on outside click / Escape.
 */
export function UploadMenu() {
  const { uploads, addFiles, dismissUpload, clearFinished } = useLibrary();
  const inputRef = useRef<HTMLInputElement>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const [open, setOpen] = useState(false);
  const [dragging, setDragging] = useState(false);

  // Dismiss the popover on an outside click or Escape.
  useEffect(() => {
    if (!open) return;
    function onPointerDown(e: MouseEvent) {
      if (rootRef.current && !rootRef.current.contains(e.target as Node)) setOpen(false);
    }
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    document.addEventListener("mousedown", onPointerDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onPointerDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  function onPick(e: ChangeEvent<HTMLInputElement>) {
    if (e.target.files) addFiles(Array.from(e.target.files));
    e.target.value = "";
  }

  function onDrop(e: DragEvent) {
    e.preventDefault();
    setDragging(false);
    if (e.dataTransfer.files?.length) addFiles(Array.from(e.dataTransfer.files));
  }

  const activeCount = uploads.filter((u) => u.phase !== "done" && u.phase !== "error").length;
  const hasFinished = uploads.some((u) => u.phase === "done" || u.phase === "error");

  return (
    <div className="upload-menu" ref={rootRef}>
      <button
        className={`upload-btn${open ? " open" : ""}`}
        onClick={() => setOpen((o) => !o)}
        aria-haspopup="dialog"
        aria-expanded={open}
      >
        <UploadIcon size={16} />
        <span>Upload</span>
        {activeCount > 0 && <span className="upload-badge">{activeCount}</span>}
        <ChevronDownIcon size={15} className="upload-chevron" />
      </button>

      {open && (
        <div className="upload-pop" role="dialog" aria-label="Upload audio">
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
        </div>
      )}
    </div>
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
