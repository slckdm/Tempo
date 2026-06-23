import { usePlayer } from "../context/PlayerContext";
import { formatTime } from "../lib/format";
import { Cover } from "./Cover";
import {
  AlertIcon,
  NextIcon,
  PauseIcon,
  PlayIcon,
  PrevIcon,
  RepeatIcon,
  ShuffleIcon,
  SpinnerIcon,
  VolumeIcon,
  VolumeMuteIcon,
} from "./Icons";

export function PlayerBar() {
  const player = usePlayer();
  const {
    current,
    isPlaying,
    loading,
    error,
    currentTime,
    duration,
    volume,
    muted,
    repeat,
    shuffle,
  } = player;

  const hasTrack = current !== null;
  const seekFill = duration > 0 ? (currentTime / duration) * 100 : 0;
  const volFill = (muted ? 0 : volume) * 100;

  return (
    <footer className="player">
      <div className="player-track">
        {hasTrack ? (
          <>
            <Cover track={current} className="cover player-cover" imageUrl={player.coverUrl} />
            <div className="player-text">
              <div className="player-title">{current.title}</div>
              {error ? (
                <div className="player-error">
                  <AlertIcon size={13} /> {error}
                </div>
              ) : (
                <div className="player-artist">{current.artist}</div>
              )}
            </div>
          </>
        ) : (
          <div className="player-text">
            <div className="player-title" style={{ color: "var(--text-faint)" }}>
              Nothing playing
            </div>
            <div className="player-artist">Pick a track from your library</div>
          </div>
        )}
      </div>

      <div className="player-center">
        <div className="player-controls">
          <button
            className={`ctrl${shuffle ? " on" : ""}`}
            onClick={player.toggleShuffle}
            disabled={!hasTrack}
            title="Shuffle"
            aria-pressed={shuffle}
          >
            <ShuffleIcon size={18} />
          </button>
          <button className="ctrl" onClick={player.prev} disabled={!hasTrack} title="Previous">
            <PrevIcon size={20} />
          </button>
          <button
            className="ctrl-play"
            onClick={player.toggle}
            disabled={!hasTrack || loading}
            title={isPlaying ? "Pause" : "Play"}
          >
            {loading ? (
              <SpinnerIcon size={20} />
            ) : isPlaying ? (
              <PauseIcon size={20} />
            ) : (
              <PlayIcon size={20} />
            )}
          </button>
          <button className="ctrl" onClick={player.next} disabled={!hasTrack} title="Next">
            <NextIcon size={20} />
          </button>
          <button
            className={`ctrl${repeat ? " on" : ""}`}
            onClick={player.toggleRepeat}
            disabled={!hasTrack}
            title="Repeat"
            aria-pressed={repeat}
          >
            <RepeatIcon size={18} />
          </button>
        </div>

        <div className="seek">
          <span className="time">{formatTime(currentTime)}</span>
          <input
            className="range filled"
            type="range"
            min={0}
            max={duration || 0}
            step={0.1}
            value={Math.min(currentTime, duration || 0)}
            style={{ "--fill": `${seekFill}%` } as React.CSSProperties}
            onChange={(e) => player.seek(Number(e.target.value))}
            disabled={!hasTrack || duration === 0}
            aria-label="Seek"
          />
          <span className="time">{formatTime(duration)}</span>
        </div>
      </div>

      <div className="player-right">
        <div className="volume">
          <button
            className="ctrl"
            onClick={player.toggleMute}
            title={muted ? "Unmute" : "Mute"}
          >
            {muted || volume === 0 ? <VolumeMuteIcon size={18} /> : <VolumeIcon size={18} />}
          </button>
          <input
            className="range filled"
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={muted ? 0 : volume}
            style={{ "--fill": `${volFill}%` } as React.CSSProperties}
            onChange={(e) => player.setVolume(Number(e.target.value))}
            aria-label="Volume"
          />
        </div>
      </div>
    </footer>
  );
}
