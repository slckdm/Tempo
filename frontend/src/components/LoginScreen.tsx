import { useState } from "react";
import type { FormEvent } from "react";

import { useAuth } from "../context/AuthContext";
import { AlertIcon, SpinnerIcon } from "./Icons";

export function LoginScreen() {
  const { authenticationError, authenticating, login, loginWithGoogle } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [passwordBusy, setPasswordBusy] = useState(false);
  const [googleBusy, setGoogleBusy] = useState(false);
  const displayedError = error ?? authenticationError;

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (passwordBusy || googleBusy || authenticating) return;
    setError(null);
    setPasswordBusy(true);
    try {
      await login(username.trim(), password);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't sign in");
      setPasswordBusy(false);
    }
  }

  async function onGoogleLogin() {
    if (passwordBusy || googleBusy || authenticating) return;
    setError(null);
    setGoogleBusy(true);
    try {
      await loginWithGoogle();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't sign in with Google");
      setGoogleBusy(false);
    }
  }

  return (
    <div className="login">
      <form className="login-card" onSubmit={onSubmit}>
        <div className="login-brand">
          <span className="brand-mark">
            <Logo />
          </span>
          <h1>Tempo</h1>
        </div>
        <p className="login-sub">Sign in to upload and listen to your music.</p>

        {displayedError && (
          <div className="login-error">
            <AlertIcon size={16} />
            <span>{displayedError}</span>
          </div>
        )}

        <button
          className="btn-google"
          type="button"
          disabled={passwordBusy || googleBusy || authenticating}
          onClick={onGoogleLogin}
        >
          {googleBusy || authenticating ? <SpinnerIcon size={18} /> : <GoogleIcon />}
          {authenticating ? "Finishing Google sign-in…" : "Continue with Google"}
        </button>

        <div className="login-divider">
          <span>or</span>
        </div>

        <div className="field">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            autoComplete="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
            autoFocus
            required
          />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            required
          />
        </div>

        <button
          className="btn-primary"
          type="submit"
          disabled={passwordBusy || googleBusy || authenticating || !username || !password}
        >
          {passwordBusy ? (
            <>
              <SpinnerIcon size={18} /> Signing in…
            </>
          ) : (
            "Sign in"
          )}
        </button>

        <p className="login-foot">Google and password sign-in are handled by Keycloak.</p>
      </form>
    </div>
  );
}

function GoogleIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true">
      <path
        fill="#4285F4"
        d="M17.64 9.205c0-.638-.057-1.252-.164-1.841H9v3.482h4.844a4.14 4.14 0 0 1-1.797 2.716v2.259h2.909c1.702-1.567 2.684-3.875 2.684-6.616Z"
      />
      <path
        fill="#34A853"
        d="M9 18c2.43 0 4.468-.806 5.956-2.179l-2.909-2.259c-.806.54-1.835.859-3.047.859-2.344 0-4.328-1.585-5.037-3.715H.956v2.332A9 9 0 0 0 9 18Z"
      />
      <path
        fill="#FBBC05"
        d="M3.963 10.706A5.41 5.41 0 0 1 3.682 9c0-.592.102-1.168.281-1.706V4.962H.956A9 9 0 0 0 0 9c0 1.452.347 2.827.956 4.038l3.007-2.332Z"
      />
      <path
        fill="#EA4335"
        d="M9 3.579c1.321 0 2.507.454 3.441 1.346l2.581-2.581C13.464.892 11.426 0 9 0A9 9 0 0 0 .956 4.962l3.007 2.332C4.672 5.164 6.656 3.579 9 3.579Z"
      />
    </svg>
  );
}

function Logo() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <rect x="6" y="5" width="2.2" height="14" rx="1.1" />
      <rect x="11" y="2" width="2.2" height="20" rx="1.1" />
      <rect x="16" y="8" width="2.2" height="8" rx="1.1" />
    </svg>
  );
}
