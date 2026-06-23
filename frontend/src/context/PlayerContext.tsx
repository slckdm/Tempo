import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import type { ReactNode } from "react";

import { fetchAudioObjectUrl, fetchCoverObjectUrl } from "../api/stream";
import { ApiError } from "../api/client";
import type { Track } from "../types";

interface PlayerContextValue {
  current: Track | null;
  isPlaying: boolean;
  loading: boolean;
  error: string | null;
  currentTime: number;
  duration: number;
  volume: number;
  muted: boolean;
  repeat: boolean;
  shuffle: boolean;
  coverUrl: string | null;
  /** Play a track; pass the surrounding list to enable next/prev navigation. */
  playTrack: (track: Track, queue?: Track[]) => void;
  toggle: () => void;
  next: () => void;
  prev: () => void;
  seek: (time: number) => void;
  setVolume: (v: number) => void;
  toggleMute: () => void;
  toggleRepeat: () => void;
  toggleShuffle: () => void;
}

const PlayerContext = createContext<PlayerContextValue | null>(null);

export function PlayerProvider({ children }: { children: ReactNode }) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  if (audioRef.current === null) audioRef.current = new Audio();

  const [current, setCurrent] = useState<Track | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolumeState] = useState(1);
  const [muted, setMuted] = useState(false);
  const [repeat, setRepeat] = useState(false);
  const [shuffle, setShuffle] = useState(false);
  const [coverUrl, setCoverUrl] = useState<string | null>(null);

  // Refs read inside the once-attached audio event handlers (avoid stale state).
  const queueRef = useRef<Track[]>([]);
  const indexRef = useRef(-1);
  const repeatRef = useRef(false);
  const shuffleRef = useRef(false);
  const loadToken = useRef(0);
  const audioUrlRef = useRef<string | null>(null);
  const coverUrlRef = useRef<string | null>(null);

  const revokeAudioUrl = useCallback(() => {
    if (audioUrlRef.current) {
      URL.revokeObjectURL(audioUrlRef.current);
      audioUrlRef.current = null;
    }
  }, []);

  const revokeCoverUrl = useCallback(() => {
    if (coverUrlRef.current) {
      URL.revokeObjectURL(coverUrlRef.current);
      coverUrlRef.current = null;
    }
  }, []);

  const loadAndPlay = useCallback(
    async (track: Track) => {
      const audio = audioRef.current!;
      const token = ++loadToken.current;
      setLoading(true);
      setError(null);
      setCurrentTime(0);
      // Show the metadata duration right away; refined once the audio loads.
      setDuration(track.duration ?? 0);

      // Cover art loads independently. Only request it when the metadata service
      // reported one, so we don't fire pointless 404s for cover-less tracks.
      revokeCoverUrl();
      setCoverUrl(null);
      if (track.hasCover) {
        void fetchCoverObjectUrl(track.urn).then((url) => {
          if (token !== loadToken.current) {
            if (url) URL.revokeObjectURL(url);
            return;
          }
          revokeCoverUrl();
          coverUrlRef.current = url;
          setCoverUrl(url);
        });
      }

      try {
        const url = await fetchAudioObjectUrl(track.urn);
        if (token !== loadToken.current) {
          URL.revokeObjectURL(url);
          return;
        }
        revokeAudioUrl();
        audioUrlRef.current = url;
        audio.src = url;
        audio.load();
        await audio.play();
        setLoading(false);
      } catch (err) {
        if (token !== loadToken.current) return;
        const message = err instanceof ApiError ? err.message : "Couldn't play this track";
        setError(message);
        setLoading(false);
        setIsPlaying(false);
      }
    },
    [revokeAudioUrl, revokeCoverUrl],
  );

  const playByIndex = useCallback(
    (index: number) => {
      const queue = queueRef.current;
      if (index < 0 || index >= queue.length) return;
      indexRef.current = index;
      const track = queue[index];
      setCurrent(track);
      void loadAndPlay(track);
    },
    [loadAndPlay],
  );

  const advance = useCallback(
    (auto: boolean) => {
      const queue = queueRef.current;
      if (queue.length === 0) return;
      const idx = indexRef.current;

      if (shuffleRef.current && queue.length > 1) {
        let r = idx;
        while (r === idx) r = Math.floor(Math.random() * queue.length);
        playByIndex(r);
        return;
      }
      const nextIdx = idx + 1;
      if (nextIdx < queue.length) {
        playByIndex(nextIdx);
      } else if (repeatRef.current) {
        playByIndex(0);
      } else if (auto) {
        setIsPlaying(false);
      } else {
        playByIndex(0); // manual "next" past the end wraps around
      }
    },
    [playByIndex],
  );

  // Attach audio element listeners once.
  useEffect(() => {
    const audio = audioRef.current!;
    const onTime = () => setCurrentTime(audio.currentTime);
    // Keep the metadata-seeded duration if the element can't determine its own.
    const onDuration = () => {
      if (Number.isFinite(audio.duration) && audio.duration > 0) setDuration(audio.duration);
    };
    const onPlay = () => setIsPlaying(true);
    const onPause = () => setIsPlaying(false);
    const onEnded = () => advance(true);
    const onVolume = () => {
      setVolumeState(audio.volume);
      setMuted(audio.muted);
    };

    audio.addEventListener("timeupdate", onTime);
    audio.addEventListener("durationchange", onDuration);
    audio.addEventListener("loadedmetadata", onDuration);
    audio.addEventListener("play", onPlay);
    audio.addEventListener("playing", onPlay);
    audio.addEventListener("pause", onPause);
    audio.addEventListener("ended", onEnded);
    audio.addEventListener("volumechange", onVolume);

    return () => {
      audio.removeEventListener("timeupdate", onTime);
      audio.removeEventListener("durationchange", onDuration);
      audio.removeEventListener("loadedmetadata", onDuration);
      audio.removeEventListener("play", onPlay);
      audio.removeEventListener("playing", onPlay);
      audio.removeEventListener("pause", onPause);
      audio.removeEventListener("ended", onEnded);
      audio.removeEventListener("volumechange", onVolume);
    };
  }, [advance]);

  // Revoke any outstanding object URLs on unmount.
  useEffect(() => {
    const audio = audioRef.current!;
    return () => {
      audio.pause();
      revokeAudioUrl();
      revokeCoverUrl();
    };
  }, [revokeAudioUrl, revokeCoverUrl]);

  const playTrack = useCallback(
    (track: Track, queue?: Track[]) => {
      const audio = audioRef.current!;
      if (current?.urn === track.urn && !error) {
        if (audio.paused) void audio.play().catch(() => undefined);
        else audio.pause();
        return;
      }
      const list = queue && queue.length > 0 ? queue : [track];
      queueRef.current = list;
      const index = Math.max(0, list.findIndex((t) => t.urn === track.urn));
      playByIndex(index);
    },
    [current, error, playByIndex],
  );

  const toggle = useCallback(() => {
    const audio = audioRef.current!;
    if (!current) return;
    if (audio.paused) void audio.play().catch(() => undefined);
    else audio.pause();
  }, [current]);

  const next = useCallback(() => advance(false), [advance]);

  const prev = useCallback(() => {
    const audio = audioRef.current!;
    if (audio.currentTime > 3) {
      audio.currentTime = 0;
      return;
    }
    const idx = indexRef.current;
    if (idx > 0) playByIndex(idx - 1);
    else if (repeatRef.current) playByIndex(queueRef.current.length - 1);
    else audio.currentTime = 0;
  }, [playByIndex]);

  const seek = useCallback((time: number) => {
    const audio = audioRef.current!;
    if (Number.isFinite(time)) audio.currentTime = time;
  }, []);

  const setVolume = useCallback((v: number) => {
    const audio = audioRef.current!;
    const clamped = Math.min(1, Math.max(0, v));
    audio.volume = clamped;
    if (clamped > 0) audio.muted = false;
  }, []);

  const toggleMute = useCallback(() => {
    const audio = audioRef.current!;
    audio.muted = !audio.muted;
  }, []);

  const toggleRepeat = useCallback(() => {
    repeatRef.current = !repeatRef.current;
    setRepeat(repeatRef.current);
  }, []);

  const toggleShuffle = useCallback(() => {
    shuffleRef.current = !shuffleRef.current;
    setShuffle(shuffleRef.current);
  }, []);

  const value = useMemo<PlayerContextValue>(
    () => ({
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
      coverUrl,
      playTrack,
      toggle,
      next,
      prev,
      seek,
      setVolume,
      toggleMute,
      toggleRepeat,
      toggleShuffle,
    }),
    [
      current, isPlaying, loading, error, currentTime, duration, volume, muted,
      repeat, shuffle, coverUrl, playTrack, toggle, next, prev, seek, setVolume,
      toggleMute, toggleRepeat, toggleShuffle,
    ],
  );

  return <PlayerContext value={value}>{children}</PlayerContext>;
}

export function usePlayer(): PlayerContextValue {
  const ctx = useContext(PlayerContext);
  if (!ctx) throw new Error("usePlayer must be used within PlayerProvider");
  return ctx;
}
