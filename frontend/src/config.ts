// Central place for the handful of knobs the frontend needs. Everything has a
// sensible default that matches the backend's local .env files, so the app runs
// with zero configuration; override via a frontend/.env file if needed.

export const config = {
  /** Same-origin proxy prefixes (see vite.config.ts). */
  managementBase: "/api/management",
  metadataBase: "/api/metadata",
  streamingBase: "/api/streaming",
  libraryBase: "/api/library",
  authBase: "/api/auth",
  /** Same-origin proxy to S3/MinIO for presigned uploads (see nginx.conf). */
  s3Base: "/api/s3",

  keycloak: {
    realm: import.meta.env.VITE_KEYCLOAK_REALM ?? "tempo",
    clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID ?? "management-service-client",
    clientSecret:
      import.meta.env.VITE_KEYCLOAK_CLIENT_SECRET ?? "zkkbWU1ff4QRLqGTx1idCVmCcLnqyzYJ",
    publicUrl: import.meta.env.VITE_KEYCLOAK_PUBLIC_URL ?? "http://localhost:8080",
    googleIdentityProviderAlias: import.meta.env.VITE_KEYCLOAK_GOOGLE_IDP_ALIAS ?? "google",
    // Keycloak client-scope NAMES (not the audience values their mappers emit).
    // Both are Optional scopes on the client; login requests both, and the
    // streaming cookie is down-scoped to `streamScope` so a stolen cookie only
    // grants streaming reads — management/metadata reject it (wrong audience).
    loginScope: "openid etc streaming",
    streamScope: "openid streaming",
  },
} as const;

export const STORAGE_KEYS = {
  session: "tempo.session.v1",
  oauthRequest: "tempo.oauth-request.v1",
  volume: "tempo.volume.v1",
} as const;
