import { cn } from "@/lib/utils";

/**
 * Loading placeholder. Uses a shimmer gradient rather than a flat pulse —
 * reads as "actively loading" rather than "static block" against the
 * dark console background.
 */
export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      aria-hidden
      className={cn(
        "animate-shimmer rounded-panel bg-gradient-to-r from-ink-raised via-line-faint to-ink-raised bg-[length:200%_100%]",
        className,
      )}
    />
  );
}
