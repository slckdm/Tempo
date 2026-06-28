import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// The Tempo backend services ship without CORS headers, so the browser cannot
// talk to them directly. The Vite dev server proxies same-origin `/api/*` paths
// to each backend, which sidesteps CORS entirely during development.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  const managementTarget = env.MANAGEMENT_URL ?? "http://127.0.0.1:8001";
  const streamingTarget = env.STREAMING_URL ?? "http://127.0.0.1:8002";
  const metadataTarget = env.METADATA_URL ?? "http://127.0.0.1:8003";
  const keycloakTarget = env.KEYCLOAK_URL ?? "http://127.0.0.1:8080";
  // Must match the host management signs presigned URLs against, so the SigV4
  // Host header still validates after proxying (changeOrigin rewrites it).
  const s3Target = env.S3_URL ?? "http://127.0.0.1:9000";

  return {
    plugins: [react()],
    server: {
      port: 5173,
      proxy: {
        "/api/management": {
          target: managementTarget,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api\/management/, ""),
        },
        "/api/streaming": {
          target: streamingTarget,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api\/streaming/, ""),
        },
        "/api/metadata": {
          target: metadataTarget,
          // The metadata service already serves under `/metadata`, so we strip
          // only the `/api` namespace prefix (unlike management/streaming, whose
          // alias segment is not part of their real path).
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
        "/api/auth": {
          target: keycloakTarget,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api\/auth/, ""),
        },
        "/api/s3": {
          target: s3Target,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api\/s3/, ""),
        },
      },
    },
  };
});
