// The three-step upload handshake with the management service:
//   1. POST /uploads          → reserve an upload, get a presigned S3 PUT URL
//   2. PUT  <presigned_url>    → browser uploads the file straight to MinIO
//   3. POST /uploads/{urn}/complete → backend verifies the object exists

import { config } from "../config";
import { resolveContentType } from "../lib/audioFiles";
import { apiJson, ApiError } from "./client";

interface CreateUploadResponse {
  /** The reserved upload's URN, e.g. `urn:mng.upload:<uuid>`. */
  upload: string;
  presigned_url: string;
}

export interface ReservedUpload {
  urn: string;
  presignedUrl: string;
  contentType: string;
}

/**
 * The presigned URL is signed by the management service against the S3 endpoint
 * *it* can reach (a container hostname in Docker), which the browser can't
 * resolve. Route the path + query through the same-origin `/api/s3` proxy, which
 * forwards to MinIO with the signed Host header intact (see nginx.conf).
 */
function toProxiedS3Url(presignedUrl: string): string {
  const u = new URL(presignedUrl);
  return `${config.s3Base}${u.pathname}${u.search}`;
}

export async function createUpload(file: File): Promise<ReservedUpload> {
  const contentType = resolveContentType(file);
  const data = await apiJson<CreateUploadResponse>(`${config.managementBase}/uploads`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      filename: file.name,
      contentType,
      size: file.size,
    }),
  });
  return {
    urn: data.upload,
    presignedUrl: toProxiedS3Url(data.presigned_url),
    contentType,
  };
}

/**
 * Upload the file to the presigned S3 URL (same-origin via the `/api/s3` proxy).
 * Uses XHR (not fetch) so we can report progress. The Content-Type must match
 * what the backend signed, or MinIO rejects the signature.
 */
export function putToPresigned(
  presignedUrl: string,
  file: File,
  contentType: string,
  onProgress?: (percent: number) => void,
): Promise<void> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("PUT", presignedUrl, true);
    xhr.setRequestHeader("Content-Type", contentType);

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable && onProgress) {
        onProgress(Math.round((event.loaded / event.total) * 100));
      }
    };
    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) resolve();
      else reject(new ApiError(`Failed to upload file to storage (${xhr.status})`, xhr.status));
    };
    xhr.onerror = () => reject(new ApiError("Network error while uploading to storage", 0));
    xhr.onabort = () => reject(new ApiError("Upload cancelled", 0));

    xhr.send(file);
  });
}

export async function completeUpload(urn: string): Promise<void> {
  await apiJson(`${config.managementBase}/uploads/${encodeURIComponent(urn)}/complete`, {
    method: "POST",
  });
}

/**
 * Delete an upload. Management removes its own row + the audio object and emits
 * an event; the metadata row and cover are cleaned up asynchronously, so the
 * caller should re-poll the library shortly after to reconcile.
 */
export async function deleteUpload(urn: string): Promise<void> {
  await apiJson(`${config.managementBase}/uploads/${encodeURIComponent(urn)}`, {
    method: "DELETE",
  });
}
