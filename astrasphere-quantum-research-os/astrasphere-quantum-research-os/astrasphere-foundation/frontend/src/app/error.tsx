"use client";

import { useEffect } from "react";

/** Route-level error boundary. Next.js mounts this on uncaught render/data errors. */
export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Structured client-side error reporting hooks in here later.
    console.error("Route error boundary caught:", error);
  }, [error]);

  return (
    <div className="flex h-screen flex-col items-center justify-center gap-4 bg-ink px-6 text-center">
      <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-danger">Signal Lost</p>
      <h1 className="font-display text-xl text-foreground">Something interrupted the console.</h1>
      <p className="max-w-sm text-sm text-foreground-muted">
        {error.message || "An unexpected error occurred while rendering this view."}
      </p>
      <button
        onClick={reset}
        className="mt-2 border border-line px-4 py-2 font-mono text-[11px] uppercase tracking-wide text-foreground transition-colors hover:border-signal hover:text-signal"
      >
        Retry
      </button>
    </div>
  );
}
