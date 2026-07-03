"use client";

import { useEffect } from "react";

import { ErrorState } from "@/components/ui/error-state";

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
    <div className="flex h-screen items-center justify-center bg-ink px-6">
      <ErrorState
        title="Something interrupted the console"
        description={error.message || "An unexpected error occurred while rendering this view."}
        onRetry={reset}
      />
    </div>
  );
}
