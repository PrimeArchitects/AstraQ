import { BarChart } from "@/components/ui/bar-chart";
import { DashboardCard } from "@/components/dashboard/dashboard-card";
import { TRENDING_TOPICS } from "@/data/mock";

/**
 * Field-wide activity by topic (paper counts) — distinct from the
 * personal ActivityTimeline. Will source from GET /analytics/activity.
 */
export function ResearchActivityCard() {
  const data = TRENDING_TOPICS.map((t) => ({ label: t.name, value: t.paperCount }));

  return (
    <DashboardCard title="Research Activity">
      <BarChart data={data} />
    </DashboardCard>
  );
}
