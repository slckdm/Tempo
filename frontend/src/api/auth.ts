// Authentication against Keycloak using the Resource Owner Password Credentials
// grant. The Tempo backend's confidential client requires a client secret, so we
// send it here (acceptable for a local pet project; see README). Tokens live in
// a module-level store + localStorage so the non-React fetch layer can read them.

import { config, STORAGE_KEYS } from "../config";
import type { AuthUser, TokenResponse } from "../types";

interface Session {
  tokens: TokenResponse;
  /** epoch ms when the tokens were obtained, used to compute expiry. */
  obtainedAt: number;
}

const tokenUrl = `${config.authBase}/realms/${config.keycloak.realm}/protocol/openid-connect/token`;

/** Cookie the access token is mirrored into; must match the streaming backend. */
const STREAM_TOKEN_COOKIE = "access_token";

let session: Session | null = loadSession();
// Re-establish the streaming cookie on a fresh page load (it may have expired
// while the tab was closed even though the refreshable session survived).
if (session) syncStreamCookie(session);
/** Coalesces concurrent refreshes into a single in-flight request. */
let refreshing: Promise<boolean> | null = null;

/** Subscribers notified whenever the session changes (login / logout / expiry). */
const listeners = new Set<() => void>();

/** Subscribe to session changes; returns an unsubscribe function. */
export function onAuthChange(listener: () => void): () => void {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

function loadSession(): Session | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.session);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Session;
    if (!parsed?.tokens?.access_token) return null;
    return parsed;
  } catch {
    return null;
  }
}

function persist(next: Session | null) {
  const hadSession = session !== null;
  session = next;
  if (next) {
    localStorage.setItem(STORAGE_KEYS.session, JSON.stringify(next));
    syncStreamCookie(next);
  } else {
    localStorage.removeItem(STORAGE_KEYS.session);
    clearStreamCookie();
  }
  // Notify on meaningful transitions (login or logout), not token refreshes.
  if (hadSession !== (next !== null)) {
    for (const listener of listeners) listener();
  }
}

// The streaming service authenticates <audio>/<img> requests — which cannot
// carry an Authorization header — via a cookie that mirrors the access token.
// Scoped to the streaming path and SameSite=Lax so it's never sent cross-site
// or to the other services; max-age tracks the token's own lifetime.
function syncStreamCookie(s: Session) {
  const maxAge = Math.max(0, Math.floor((accessExpiresAt(s) - Date.now()) / 1000));
  const secure = location.protocol === "https:" ? "; Secure" : "";
  document.cookie =
    `${STREAM_TOKEN_COOKIE}=${s.tokens.access_token}` +
    `; Path=${config.streamingBase}; Max-Age=${maxAge}; SameSite=Lax${secure}`;
}

function clearStreamCookie() {
  document.cookie = `${STREAM_TOKEN_COOKIE}=; Path=${config.streamingBase}; Max-Age=0; SameSite=Lax`;
}

function accessExpiresAt(s: Session): number {
  return s.obtainedAt + s.tokens.expires_in * 1000;
}

function refreshExpiresAt(s: Session): number {
  return s.obtainedAt + s.tokens.refresh_expires_in * 1000;
}

/** Decode a JWT payload (no verification — the backend verifies for real). */
function decodeJwt(token: string): Record<string, unknown> | null {
  try {
    const payload = token.split(".")[1];
    const json = atob(payload.replace(/-/g, "+").replace(/_/g, "/"));
    return JSON.parse(decodeURIComponent(escape(json)));
  } catch {
    return null;
  }
}

export class AuthError extends Error {}

async function requestToken(body: Record<string, string>): Promise<TokenResponse> {
  const res = await fetch(tokenUrl, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: config.keycloak.clientId,
      client_secret: config.keycloak.clientSecret,
      ...body,
    }),
  });

  if (!res.ok) {
    let description = `Authentication error (${res.status})`;
    try {
      const data = (await res.json()) as { error?: string; error_description?: string };
      if (data.error === "invalid_grant") description = "Invalid username or password";
      else if (data.error_description) description = data.error_description;
      else if (data.error) description = data.error;
    } catch {
      /* keep default */
    }
    throw new AuthError(description);
  }

  return (await res.json()) as TokenResponse;
}

export function userFromToken(token: string): AuthUser | null {
  const payload = decodeJwt(token);
  if (!payload || typeof payload.preferred_username !== "string") return null;
  const first = typeof payload.given_name === "string" ? payload.given_name : "";
  const last = typeof payload.family_name === "string" ? payload.family_name : "";
  const name = [first, last].filter(Boolean).join(" ") || payload.preferred_username;
  return {
    username: payload.preferred_username,
    name,
    email: typeof payload.email === "string" ? payload.email : undefined,
  };
}

export async function login(username: string, password: string): Promise<AuthUser> {
  const tokens = await requestToken({ grant_type: "password", username, password, scope: "openid" });
  persist({ tokens, obtainedAt: Date.now() });
  const user = userFromToken(tokens.access_token);
  if (!user) throw new AuthError("Could not read user data from the token");
  return user;
}

async function doRefresh(): Promise<boolean> {
  if (!session) return false;
  if (Date.now() >= refreshExpiresAt(session) - 5_000) {
    persist(null);
    return false;
  }
  try {
    const tokens = await requestToken({
      grant_type: "refresh_token",
      refresh_token: session.tokens.refresh_token,
    });
    persist({ tokens, obtainedAt: Date.now() });
    return true;
  } catch {
    persist(null);
    return false;
  }
}

/** Returns a valid access token, refreshing proactively, or null if logged out. */
export async function getAccessToken(): Promise<string | null> {
  if (!session) return null;
  if (Date.now() < accessExpiresAt(session) - 15_000) {
    return session.tokens.access_token;
  }
  refreshing ??= doRefresh().finally(() => {
    refreshing = null;
  });
  const ok = await refreshing;
  return ok && session ? session.tokens.access_token : null;
}

/** Force a refresh after a 401; returns the new token or null. */
export async function forceRefresh(): Promise<string | null> {
  refreshing ??= doRefresh().finally(() => {
    refreshing = null;
  });
  const ok = await refreshing;
  return ok && session ? session.tokens.access_token : null;
}

export function currentUser(): AuthUser | null {
  if (!session) return null;
  if (Date.now() >= refreshExpiresAt(session)) {
    persist(null);
    return null;
  }
  return userFromToken(session.tokens.access_token);
}

export function logout() {
  persist(null);
}
