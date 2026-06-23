// Thin fetch wrapper: injects the bearer token, transparently refreshes once on
// 401, and unwraps the backend's JSend envelope ({ status, data, message }).

import { forceRefresh, getAccessToken, logout } from "./auth";

export class ApiError extends Error {
  status: number;
  /** True when the session is gone and the user must log in again. */
  unauthorized: boolean;

  constructor(message: string, status: number, unauthorized = false) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.unauthorized = unauthorized;
  }
}

/** Fetch with the current bearer token, retrying once after a token refresh. */
export async function authedFetch(input: string, init: RequestInit = {}): Promise<Response> {
  const token = await getAccessToken();
  if (!token) {
    logout();
    throw new ApiError("Session expired, please sign in again", 401, true);
  }

  const withAuth = (bearer: string): RequestInit => ({
    ...init,
    headers: { ...init.headers, Authorization: `Bearer ${bearer}` },
  });

  let res = await fetch(input, withAuth(token));
  if (res.status === 401) {
    const fresh = await forceRefresh();
    if (!fresh) {
      logout();
      throw new ApiError("Session expired, please sign in again", 401, true);
    }
    res = await fetch(input, withAuth(fresh));
    if (res.status === 401) {
      logout();
      throw new ApiError("Session expired, please sign in again", 401, true);
    }
  }
  return res;
}

const STATUS_MESSAGES: Record<number, string> = {
  403: "Access denied",
  404: "Not found",
  415: "File is not audio",
  422: "Invalid request data",
  500: "Internal server error",
};

/** Perform an authed request and unwrap a JSend success payload. */
export async function apiJson<T>(input: string, init: RequestInit = {}): Promise<T> {
  const res = await authedFetch(input, init);

  let body: unknown = null;
  try {
    body = await res.json();
  } catch {
    /* some endpoints may return an empty body */
  }

  const envelope = body as { status?: string; data?: T; message?: string } | null;

  if (!res.ok || (envelope && envelope.status && envelope.status !== "success")) {
    const message =
      envelope?.message ?? STATUS_MESSAGES[res.status] ?? `Request failed (${res.status})`;
    throw new ApiError(message, res.status, res.status === 401);
  }

  return (envelope?.data ?? (body as T)) as T;
}
