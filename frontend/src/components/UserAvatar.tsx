import { useEffect, useState } from "react";
import Avatar from "boring-avatars";

// Warm, on-brand palette so the generated avatars harmonize with the yellow theme.
const AVATAR_COLORS = ["#ffc83d", "#ff9d2e", "#ffe08a", "#f59e0b", "#ff7a59"];

/**
 * Deterministic, generated user avatar (boring-avatars). The same `name` always
 * produces the same avatar, so a user keeps a stable identity across sessions.
 */
export function UserAvatar({
  name,
  imageUrl,
  size = 38,
}: {
  name: string;
  imageUrl?: string;
  size?: number;
}) {
  const [imageFailed, setImageFailed] = useState(false);

  useEffect(() => setImageFailed(false), [imageUrl]);

  if (imageUrl && !imageFailed) {
    return (
      <img
        className="avatar-image"
        src={imageUrl}
        alt=""
        width={size}
        height={size}
        referrerPolicy="no-referrer"
        onError={() => setImageFailed(true)}
      />
    );
  }

  return <Avatar name={name} variant="beam" size={size} colors={AVATAR_COLORS} />;
}
