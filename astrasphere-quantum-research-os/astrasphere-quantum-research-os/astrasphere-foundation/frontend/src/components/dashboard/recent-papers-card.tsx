import { FileText } from "lucide-react";

import { DashboardCard } from "@/components/dashboard/dashboard-card";
import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/ui/empty-state";
import { Progress } from "@/components/ui/progress";
import { RECENT_PAPERS, type Paper } from "@/data/mock";

const STATUS_VARIANT: Record<Paper["status"], "neutral" | "success" | "info" | "warning"> = {
  new: "info",
  reading: "warning",
  reviewed: "success",
  saved: "neutral",
};

/** Shows the most recently added/touched papers. Will source from GET /papers?sort=recent. */
export function RecentPapersCard() {
  if (RECENT_PAPERS.length === 0) {
    return (
      <DashboardCard title="Recent Papers">
        <EmptyState
          icon={FileText}
          title="No papers yet"
          description="Upload your first paper to start building your library."
        />
      </DashboardCard>
    );
  }

  return (
    <DashboardCard title="Recent Papers" action={{ label: "View all", href: "/my-papers" }}>
      <ul className="divide-y divide-line-faint">
        {RECENT_PAPERS.map((paper) => (
          <li key={paper.id} className="py-3 first:pt-0 last:pb-0">
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="truncate text-body-sm font-medium text-foreground">{paper.title}</p>
                <p className="mt-0.5 truncate text-body-sm text-foreground-faint">
                  {paper.authors.join(", ")} &middot; {paper.venue} &middot; {paper.year}
                </p>
              </div>
              <Badge variant={STATUS_VARIANT[paper.status]} className="shrink-0">
                {paper.status}
              </Badge>
            </div>
            {paper.progress !== undefined && (
              <Progress
                value={paper.progress}
                className="mt-2"
                aria-label={`Reading progress for ${paper.title}`}
              />
            )}
          </li>
        ))}
      </ul>
    </DashboardCard>
  );
}
