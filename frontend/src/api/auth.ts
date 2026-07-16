// Authentication against Keycloak using Google-brokered Authorization Code +
// PKCE or the existing password grant. Tokens live in a module-level store and
// localStorage so the non-React fetch layer can read them.

import { config, STORAGE_KEYS } from "../config";
import type { AuthUser, TokenResponse } from "../types";

interface Session {
  tokens: TokenResponse;
  /** epoch ms when the tokens were obtained, used to compute expiry. */
  obtainedAt: number;
}

interface OAuthRequest {
  state: string;
  nonce: string;
  codeVerifier: string;
  redirectUri: string;
  createdAt: number;
}

const tokenUrl = `${config.authBase}/realms/${config.keycloak.realm}/protocol/openid-connect/token`;
const authorizationUrl = `${config.keycloak.publicUrl}/realms/${config.keycloak.realm}/protocol/openid-connect/auth`;
const OAUTH_REQUEST_MAX_AGE = 10 * 60 * 1000;

/** Cookie the access token is mirrored into; must match the streaming backend. */
const STREAM_TOKEN_COOKIE = "access_token";

let session: Session | null = loadSession();
/** Coalesces concurrent refreshes into a single in-flight request. */
let refreshing: Promise<boolean> | null = null;
/** Coalesces callback handling when React StrictMode mounts twice in development. */
let oauthCallbackHandling: Promise<AuthUser | null> | null = null;

// Stream-scoped access token mirrored into the streaming cookie for the <audio>
// element. It carries only the streaming audience, so a stolen cookie grants
// streaming reads and nothing else. Minted lazily (see getStreamToken) by
// down-scoping the session's refresh token; the broad session token stays the
// bearer for the management/metadata APIs.
let streamToken: { value: string; expiresAt: number } | null = null;
/** Coalesces concurrent stream-token mints into a single in-flight request. */
let streamMinting: Promise<string | null> | null = null;

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
  } else {
    localStorage.removeItem(STORAGE_KEYS.session);
    clearStreamCookie();
  }
  // Notify on meaningful transitions (login or logout), not token refreshes.
  if (hadSession !== (next !== null)) {
    for (const listener of listeners) listener();
  }
}

// The <audio> element can't send an Authorization header, so the streaming
// service reads the token from a cookie. We mirror a *stream-scoped* token here
// (never the API bearer): down-scoped to the streaming audience, path-scoped to
// the streaming service, and SameSite=Lax — so a stolen cookie only grants
// streaming reads, and management/metadata reject it (wrong audience).
async function mintStreamToken(): Promise<string | null> {
  const current = session;
  if (!current) return null;
  try {
    const tokens = await requestToken({
      grant_type: "refresh_token",
      refresh_token: current.tokens.refresh_token,
      scope: config.keycloak.streamScope,
    });
    // A concurrent refresh may have rotated the session; re-read it and keep its
    // refresh token current so both flows stay valid.
    if (!session) return null;
    session = { ...session, tokens: { ...session.tokens, refresh_token: tokens.refresh_token } };
    localStorage.setItem(STORAGE_KEYS.session, JSON.stringify(session));
    const expiresAt = Date.now() + tokens.expires_in * 1000;
    streamToken = { value: tokens.access_token, expiresAt };
    writeStreamCookie(tokens.access_token, expiresAt);
    return tokens.access_token;
  } catch {
    return null;
  }
}

/** Returns a valid stream-scoped token, (re)writing the cookie, or null. */
export async function getStreamToken(): Promise<string | null> {
  if (!session) return null;
  if (streamToken && Date.now() < streamToken.expiresAt - 15_000) return streamToken.value;
  streamMinting ??= mintStreamToken().finally(() => {
    streamMinting = null;
  });
  return streamMinting;
}

function writeStreamCookie(token: string, expiresAt: number) {
  const maxAge = Math.max(0, Math.floor((expiresAt - Date.now()) / 1000));
  const secure = location.protocol === "https:" ? "; Secure" : "";
  document.cookie =
    `${STREAM_TOKEN_COOKIE}=${token}` +
    `; Path=${config.streamingBase}; Max-Age=${maxAge}; SameSite=Lax${secure}`;
}

function clearStreamCookie() {
  streamToken = null;
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
  const clientCredentials: Record<string, string> = {
    client_id: config.keycloak.clientId,
  };
  if (config.keycloak.clientSecret) {
    clientCredentials.client_secret = config.keycloak.clientSecret;
  }

  const res = await fetch(tokenUrl, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      ...clientCredentials,
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

function stringClaim(
  claim: string,
  payload: Record<string, unknown>,
  identity: Record<string, unknown> | null,
): string | undefined {
  const value = payload[claim] ?? identity?.[claim];
  return typeof value === "string" && value ? value : undefined;
}

export function userFromToken(token: string, identityToken?: string): AuthUser | null {
  const payload = decodeJwt(token);
  if (!payload) return null;
  const identity = identityToken ? decodeJwt(identityToken) : null;
  const username = stringClaim("preferred_username", payload, identity);
  const id = stringClaim("sub", payload, identity);
  if (!username || !id) return null;
  const firstName = stringClaim("given_name", payload, identity);
  const lastName = stringClaim("family_name", payload, identity);
  const name = [firstName, lastName].filter(Boolean).join(" ") || username;
  return {
    id,
    username,
    name,
    email: stringClaim("email", payload, identity),
    avatarUrl: stringClaim("picture", payload, identity),
  };
}

export async function login(username: string, password: string): Promise<AuthUser> {
  const tokens = await requestToken({
    grant_type: "password",
    username,
    password,
    scope: config.keycloak.loginScope,
  });
  persist({ tokens, obtainedAt: Date.now() });
  const user = userFromToken(tokens.access_token, tokens.id_token);
  if (!user) throw new AuthError("Could not read user data from the token");
  return user;
}

function encodeBase64Url(bytes: Uint8Array): string {
  let value = "";
  for (const byte of bytes) value += String.fromCharCode(byte);
  return btoa(value).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function randomBase64Url(): string {
  return encodeBase64Url(crypto.getRandomValues(new Uint8Array(32)));
}

async function createCodeChallenge(codeVerifier: string): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(codeVerifier));
  return encodeBase64Url(new Uint8Array(digest));
}

function oauthRedirectUri(): string {
  return `${location.origin}${location.pathname}`;
}

function readOAuthRequest(): OAuthRequest | null {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEYS.oauthRequest);
    if (!raw) return null;
    const request = JSON.parse(raw) as OAuthRequest;
    if (
      !request.state ||
      !request.nonce ||
      !request.codeVerifier ||
      !request.redirectUri ||
      typeof request.createdAt !== "number" ||
      Date.now() - request.createdAt > OAUTH_REQUEST_MAX_AGE
    ) {
      return null;
    }
    return request;
  } catch {
    return null;
  }
}

function clearOAuthCallbackUrl() {
  const url = new URL(location.href);
  for (const parameter of [
    "code",
    "state",
    "session_state",
    "iss",
    "error",
    "error_description",
  ]) {
    url.searchParams.delete(parameter);
  }
  history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);
}

export function hasOAuthCallback(): boolean {
  const parameters = new URLSearchParams(location.search);
  return parameters.has("code") || parameters.has("error");
}

export async function loginWithGoogle(): Promise<void> {
  const codeVerifier = randomBase64Url();
  const request: OAuthRequest = {
    state: randomBase64Url(),
    nonce: randomBase64Url(),
    codeVerifier,
    redirectUri: oauthRedirectUri(),
    createdAt: Date.now(),
  };
  sessionStorage.setItem(STORAGE_KEYS.oauthRequest, JSON.stringify(request));

  const parameters = new URLSearchParams({
    client_id: config.keycloak.clientId,
    redirect_uri: request.redirectUri,
    response_type: "code",
    response_mode: "query",
    scope: config.keycloak.loginScope,
    state: request.state,
    nonce: request.nonce,
    code_challenge: await createCodeChallenge(codeVerifier),
    code_challenge_method: "S256",
    kc_idp_hint: config.keycloak.googleIdentityProviderAlias,
  });
  location.assign(`${authorizationUrl}?${parameters}`);
}

async function processOAuthCallback(): Promise<AuthUser | null> {
  if (!hasOAuthCallback()) return null;

  const parameters = new URLSearchParams(location.search);
  const request = readOAuthRequest();
  try {
    const error = parameters.get("error");
    if (error) {
      if (error === "access_denied") throw new AuthError("Google sign-in was cancelled");
      throw new AuthError(parameters.get("error_description") ?? `Google sign-in failed: ${error}`);
    }
    if (!request || parameters.get("state") !== request.state) {
      throw new AuthError("Google sign-in response could not be verified. Please try again.");
    }

    const code = parameters.get("code");
    if (!code) throw new AuthError("Google sign-in did not return an authorization code");

    const tokens = await requestToken({
      grant_type: "authorization_code",
      code,
      redirect_uri: request.redirectUri,
      code_verifier: request.codeVerifier,
    });
    const identity = tokens.id_token ? decodeJwt(tokens.id_token) : null;
    if (!identity || identity.nonce !== request.nonce) {
      throw new AuthError("Google sign-in identity could not be verified");
    }

    const user = userFromToken(tokens.access_token, tokens.id_token);
    if (!user) throw new AuthError("Could not read user data from the token");
    persist({ tokens, obtainedAt: Date.now() });
    return user;
  } finally {
    sessionStorage.removeItem(STORAGE_KEYS.oauthRequest);
    clearOAuthCallbackUrl();
  }
}

export function completeOAuthLogin(): Promise<AuthUser | null> {
  oauthCallbackHandling ??= processOAuthCallback();
  return oauthCallbackHandling;
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
    persist({
      tokens: { ...tokens, id_token: tokens.id_token ?? session.tokens.id_token },
      obtainedAt: Date.now(),
    });
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
  return userFromToken(session.tokens.access_token, session.tokens.id_token);
}

export function logout() {
  persist(null);
}
