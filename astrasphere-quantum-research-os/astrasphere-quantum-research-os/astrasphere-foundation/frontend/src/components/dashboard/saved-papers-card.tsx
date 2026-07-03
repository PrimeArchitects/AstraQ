import { Bookmark } from "lucide-react";

import { DashboardCard } from "@/components/dashboard/dashboard-card";
import { EmptyState } from "@/components/ui/empty-state";
import { SAVED_PAPERS } from "@/data/mock";

/** Bookmarked papers for later reading. Will source from GET /papers?status=saved. */
export function SavedPapersCard() {
  if (SAVED_PAPERS.length === 0) {
    return (
      <DashboardCard title="Saved Papers">
        <EmptyState
          icon={Bookmark}
          title="Nothing saved yet"
          description="Bookmark papers to read later."
        />
      </DashboardCard>
    );
  }

  return (
    <DashboardCard title="Saved Papers" action={{ label: "View all", href: "/bookmarks" }}>
      <ul className="space-y-3">
        {SAVED_PAPERS.map((paper) => (
          <li key={paper.id} className="flex items-start gap-2.5">
            <Bookmark className="mt-0.5 h-3.5 w-3.5 shrink-0 text-entangled" aria-hidden />
            <div className="min-w-0">
              <p className="truncate text-body-sm text-foreground">{paper.title}</p>
              <p className="mt-0.5 flex flex-wrap gap-1">
                {paper.tags.map((tag) => (
                  <span
                    key={tag}
                    className="font-mono text-label uppercase tracking-widest text-foreground-faint"
                  >
                    #{tag}
                  </span>
                ))}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </DashboardCard>
  );
}
