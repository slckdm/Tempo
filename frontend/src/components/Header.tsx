import { useAuth } from "../context/AuthContext";
import { LogoutIcon } from "./Icons";
import { UserAvatar } from "./UserAvatar";

export function Header() {
  const { user, logout } = useAuth();
  const seed = user?.username || user?.name || "user";

  return (
    <header className="header">
      <div className="brand">
        <span className="brand-mark">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <rect x="6" y="5" width="2.2" height="14" rx="1.1" />
            <rect x="11" y="2" width="2.2" height="20" rx="1.1" />
            <rect x="16" y="8" width="2.2" height="8" rx="1.1" />
          </svg>
        </span>
        Tempo
        <span className="brand-sub">music library</span>
      </div>

      <div className="user-box">
        <div className="user-meta">
          <div className="user-name">{user?.name}</div>
          {user?.email && <div className="user-mail">{user.email}</div>}
        </div>
        <span className="avatar" title={user?.name}>
          <UserAvatar name={seed} imageUrl={user?.avatarUrl} size={38} />
        </span>
        <button className="icon-btn" onClick={logout} title="Sign out" aria-label="Sign out">
          <LogoutIcon size={18} />
        </button>
      </div>
    </header>
  );
}
