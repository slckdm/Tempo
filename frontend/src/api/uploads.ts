// The three-step upload handshake with the management service:
//   1. POST /uploads          → reserve an upload, get a presigned S3 PUT URL
//   2. PUT  <presigned_url>    → browser uploads the file straight to MinIO
//   3. POST /uploads/{urn}/complete → backend verifies the object exists

import { config } from "../config";
import { resolveContentType } from "../lib/audioFiles";
import { apiJson, ApiError } from "./client";

interface CreateUploadResponse {
  upload: { urn: string };
  presigned_url: string;
}

export interface ReservedUpload {
  urn: string;
  presignedUrl: string;
  contentType: string;
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
  return { urn: data.upload.urn, presignedUrl: data.presigned_url, contentType };
}

/**
 * Upload the file to the presigned S3 URL. Uses XHR (not fetch) so we can report
 * progress. The PUT goes directly to MinIO, whose default CORS policy allows it;
 * the Content-Type must match what the backend signed.
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
