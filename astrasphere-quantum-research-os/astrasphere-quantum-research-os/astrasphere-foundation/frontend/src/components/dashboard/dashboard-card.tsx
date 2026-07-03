import Link from "next/link";
import type { Route } from "next";
import type { ReactNode } from "react";

import { Panel } from "@/components/ui/panel";

interface DashboardCardProps {
  title: string;
  action?: { label: string; href: Route };
  children: ReactNode;
  className?: string;
}

/** Standard header + body treatment for every dashboard card — keeps the grid visually consistent. */
export function DashboardCard({ title, action, children, className }: DashboardCardProps) {
  return (
    <Panel className={className}>
      <div className="mb-4 flex items-center justify-between">
        <h2 className="font-display text-title text-foreground">{title}</h2>
        {action && (
          <Link
            href={action.href}
            className="text-body-sm text-foreground-faint transition-colors hover:text-signal"
          >
            {action.label}
          </Link>
        )}
      </div>
      {children}
    </Panel>
  );
}
