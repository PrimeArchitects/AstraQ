import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex h-screen flex-col items-center justify-center gap-4 bg-ink px-6 text-center">
      <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-foreground-faint">404</p>
      <h1 className="font-display text-xl text-foreground">No signal at this coordinate.</h1>
      <Link
        href="/"
        className="mt-2 border border-line px-4 py-2 font-mono text-[11px] uppercase tracking-wide text-foreground transition-colors hover:border-signal hover:text-signal"
      >
        Return to console
      </Link>
    </div>
  );
}
