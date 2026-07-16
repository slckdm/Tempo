import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from "react";
import type { ReactNode } from "react";

import {
  completeOAuthLogin,
  currentUser,
  hasOAuthCallback,
  login as apiLogin,
  loginWithGoogle as apiLoginWithGoogle,
  logout as apiLogout,
  onAuthChange,
} from "../api/auth";
import type { AuthUser } from "../types";

interface AuthContextValue {
  user: AuthUser | null;
  login: (username: string, password: string) => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  logout: () => void;
  authenticationError: string | null;
  authenticating: boolean;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(() => currentUser());
  const [authenticationError, setAuthenticationError] = useState<string | null>(null);
  const [authenticating, setAuthenticating] = useState(() => hasOAuthCallback());
  const oauthCallbackExpected = useRef(hasOAuthCallback());

  // Keep React state in sync with the token store, including expiry-driven
  // logouts triggered deep inside the fetch layer.
  useEffect(() => onAuthChange(() => setUser(currentUser())), []);

  useEffect(() => {
    if (!oauthCallbackExpected.current) return;
    let active = true;
    void completeOAuthLogin()
      .then((authenticatedUser) => {
        if (active && authenticatedUser) setUser(authenticatedUser);
      })
      .catch((error: unknown) => {
        if (active) {
          setAuthenticationError(error instanceof Error ? error.message : "Google sign-in failed");
        }
      })
      .finally(() => {
        if (active) setAuthenticating(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    setAuthenticationError(null);
    const u = await apiLogin(username, password);
    setUser(u);
  }, []);

  const loginWithGoogle = useCallback(async () => {
    setAuthenticationError(null);
    setAuthenticating(true);
    try {
      await apiLoginWithGoogle();
    } catch (error) {
      setAuthenticating(false);
      throw error;
    }
  }, []);

  const logout = useCallback(() => apiLogout(), []);

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      login,
      loginWithGoogle,
      logout,
      authenticationError,
      authenticating,
    }),
    [user, login, loginWithGoogle, logout, authenticationError, authenticating],
  );

  return <AuthContext value={value}>{children}</AuthContext>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
