import { SearchX } from "lucide-react";
import Link from "next/link";

import { EmptyState } from "@/components/ui/empty-state";

export default function NotFound() {
  return (
    <div className="flex h-screen items-center justify-center bg-ink px-6">
      <EmptyState
        icon={SearchX}
        title="No signal at this coordinate"
        description="The page you're looking for doesn't exist."
        action={
          <Link
            href="/"
            className="mt-1 border border-line px-4 py-2 font-mono text-label uppercase tracking-widest text-foreground transition-colors hover:border-signal hover:text-signal"
          >
            Return to console
          </Link>
        }
      />
    </div>
  );
}
