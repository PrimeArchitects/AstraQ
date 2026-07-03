import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description?: string;
  action?: ReactNode;
}

/** Consistent "nothing here yet" treatment — reserved routes, empty lists, no search results. */
export function EmptyState({ icon: Icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 border border-dashed border-line px-6 py-16 text-center">
      <Icon className="h-8 w-8 text-foreground-faint" strokeWidth={1.5} aria-hidden />
      <p className="font-display text-title text-foreground">{title}</p>
      {description && <p className="max-w-sm text-body-sm text-foreground-muted">{description}</p>}
      {action}
    </div>
  );
}
