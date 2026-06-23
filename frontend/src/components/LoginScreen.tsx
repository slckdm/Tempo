import { useState } from "react";
import type { FormEvent } from "react";

import { useAuth } from "../context/AuthContext";
import { AlertIcon, SpinnerIcon } from "./Icons";

export function LoginScreen() {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (busy) return;
    setError(null);
    setBusy(true);
    try {
      await login(username.trim(), password);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't sign in");
      setBusy(false);
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

        {error && (
          <div className="login-error">
            <AlertIcon size={16} />
            <span>{error}</span>
          </div>
        )}

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

        <button className="btn-primary" type="submit" disabled={busy || !username || !password}>
          {busy ? (
            <>
              <SpinnerIcon size={18} /> Signing in…
            </>
          ) : (
            "Sign in"
          )}
        </button>

        <p className="login-foot">
          Uses a Keycloak user account in realm <code>muslick</code>. Requires a real
          user (not a service account) with first name, last name, and e-mail set.
        </p>
      </form>
    </div>
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
