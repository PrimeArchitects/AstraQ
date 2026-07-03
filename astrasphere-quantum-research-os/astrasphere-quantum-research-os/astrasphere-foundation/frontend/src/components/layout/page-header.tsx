import type { ReactNode } from "react";

interface PageHeaderProps {
  title: string;
  description?: string;
  action?: ReactNode;
}

/** Consistent title block for every top-level route below the dashboard. */
export function PageHeader({ title, description, action }: PageHeaderProps) {
  return (
    <div className="mb-8 flex flex-col items-start justify-between gap-4 border-b border-line pb-6 sm:flex-row sm:items-center">
      <div>
        <h1 className="font-display text-display-sm text-foreground">{title}</h1>
        {description && <p className="mt-1.5 text-body-sm text-foreground-muted">{description}</p>}
      </div>
      {action}
    </div>
  );
}
