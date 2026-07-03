import { DashboardCard } from "@/components/dashboard/dashboard-card";
import { Progress } from "@/components/ui/progress";
import { READING_PROGRESS } from "@/data/mock";

/** Weekly reading goal tracker. Will source from GET /users/me/reading-stats. */
export function ReadingProgressCard() {
  const { papersReadThisWeek, weeklyGoal, papersInProgress, streakDays } = READING_PROGRESS;
  const pct = Math.round((papersReadThisWeek / weeklyGoal) * 100);

  return (
    <DashboardCard title="Reading Progress">
      <p className="font-mono text-data-lg text-foreground">
        {papersReadThisWeek}
        <span className="text-body text-foreground-faint"> / {weeklyGoal} this week</span>
      </p>
      <Progress value={pct} className="mt-3" aria-label="Weekly reading goal progress" />
      <dl className="mt-4 grid grid-cols-2 gap-3 border-t border-line-faint pt-4">
        <div>
          <dt className="font-mono text-label uppercase tracking-widest text-foreground-faint">
            In progress
          </dt>
          <dd className="mt-0.5 font-mono text-body text-foreground">{papersInProgress}</dd>
        </div>
        <div>
          <dt className="font-mono text-label uppercase tracking-widest text-foreground-faint">
            Streak
          </dt>
          <dd className="mt-0.5 font-mono text-body text-foreground">{streakDays} days</dd>
        </div>
      </dl>
    </DashboardCard>
  );
}
