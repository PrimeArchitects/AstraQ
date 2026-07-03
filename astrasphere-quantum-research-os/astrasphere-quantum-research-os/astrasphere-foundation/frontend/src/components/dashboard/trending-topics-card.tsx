import { TrendingUp } from "lucide-react";

import { DashboardCard } from "@/components/dashboard/dashboard-card";
import { Sparkline } from "@/components/ui/sparkline";
import { TRENDING_TOPICS } from "@/data/mock";

/** Topic velocity across the field. Will source from GET /topics/trending. */
export function TrendingTopicsCard() {
  return (
    <DashboardCard title="Trending Quantum Topics">
      <ul className="divide-y divide-line-faint">
        {TRENDING_TOPICS.map((topic) => (
          <li
            key={topic.id}
            className="flex items-center justify-between gap-4 py-3 first:pt-0 last:pb-0"
          >
            <div className="min-w-0">
              <p className="truncate text-body-sm font-medium text-foreground">{topic.name}</p>
              <p className="mt-0.5 font-mono text-data text-foreground-faint">
                {topic.paperCount} papers
              </p>
            </div>
            <div className="flex shrink-0 items-center gap-2">
              <Sparkline data={topic.trend} className="text-signal" />
              <span className="flex items-center gap-0.5 font-mono text-data text-signal">
                <TrendingUp className="h-3 w-3" aria-hidden />+{topic.changePct}%
              </span>
            </div>
          </li>
        ))}
      </ul>
    </DashboardCard>
  );
}
