import { AlertTriangle } from "lucide-react";

import { Button } from "@/components/ui/button";

interface ErrorStateProps {
  title?: string;
  description?: string;
  onRetry?: () => void;
}

/** Consistent error treatment for failed data-fetch regions (cards, panels, tables). */
export function ErrorState({
  title = "Couldn't load this data",
  description = "Something went wrong while fetching this section.",
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 border border-line px-6 py-12 text-center">
      <AlertTriangle className="h-6 w-6 text-danger" strokeWidth={1.5} aria-hidden />
      <p className="font-display text-title text-foreground">{title}</p>
      <p className="max-w-sm text-body-sm text-foreground-muted">{description}</p>
      {onRetry && (
        <Button variant="outline" size="sm" onClick={onRetry}>
          Retry
        </Button>
      )}
    </div>
  );
}
