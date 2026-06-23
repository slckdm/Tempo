import Avatar from "boring-avatars";

// Warm, on-brand palette so the generated avatars harmonize with the yellow theme.
const AVATAR_COLORS = ["#ffc83d", "#ff9d2e", "#ffe08a", "#f59e0b", "#ff7a59"];

/**
 * Deterministic, generated user avatar (boring-avatars). The same `name` always
 * produces the same avatar, so a user keeps a stable identity across sessions.
 */
export function UserAvatar({ name, size = 38 }: { name: string; size?: number }) {
  return <Avatar name={name} variant="beam" size={size} colors={AVATAR_COLORS} />;
}
