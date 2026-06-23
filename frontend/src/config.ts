// Central place for the handful of knobs the frontend needs. Everything has a
// sensible default that matches the backend's local .env files, so the app runs
// with zero configuration; override via a frontend/.env file if needed.

export const config = {
  /** Same-origin proxy prefixes (see vite.config.ts). */
  managementBase: "/api/management",
  metadataBase: "/api/metadata",
  streamingBase: "/api/streaming",
  authBase: "/api/auth",

  keycloak: {
    realm: import.meta.env.VITE_KEYCLOAK_REALM ?? "muslick",
    clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID ?? "management-service-client",
    clientSecret:
      import.meta.env.VITE_KEYCLOAK_CLIENT_SECRET ?? "zkkbWU1ff4QRLqGTx1idCVmCcLnqyzYJ",
  },
} as const;

export const STORAGE_KEYS = {
  session: "tempo.session.v1",
} as const;
