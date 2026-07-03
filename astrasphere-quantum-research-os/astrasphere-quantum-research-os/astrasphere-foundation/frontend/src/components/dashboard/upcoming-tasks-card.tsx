import { CheckSquare, Square } from "lucide-react";

import { DashboardCard } from "@/components/dashboard/dashboard-card";
import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/ui/empty-state";
import { UPCOMING_TASKS, type Task } from "@/data/mock";

const PRIORITY_VARIANT: Record<Task["priority"], "critical" | "warning" | "neutral"> = {
  high: "critical",
  medium: "warning",
  low: "neutral",
};

/** Personal task list. Will source from GET /tasks?status=open. */
export function UpcomingTasksCard() {
  const openTasks = UPCOMING_TASKS.filter((t) => !t.done);

  if (openTasks.length === 0) {
    return (
      <DashboardCard title="Upcoming Tasks">
        <EmptyState
          icon={CheckSquare}
          title="All caught up"
          description="No open tasks right now."
        />
      </DashboardCard>
    );
  }

  return (
    <DashboardCard title="Upcoming Tasks">
      <ul className="space-y-3">
        {UPCOMING_TASKS.map((task) => (
          <li key={task.id} className="flex items-start gap-2.5">
            {task.done ? (
              <CheckSquare className="mt-0.5 h-4 w-4 shrink-0 text-signal" aria-hidden />
            ) : (
              <Square className="mt-0.5 h-4 w-4 shrink-0 text-foreground-faint" aria-hidden />
            )}
            <div className="min-w-0 flex-1">
              <p
                className={
                  task.done
                    ? "text-body-sm text-foreground-faint line-through"
                    : "text-body-sm text-foreground"
                }
              >
                {task.title}
              </p>
              <div className="mt-1 flex items-center gap-2">
                <Badge variant={PRIORITY_VARIANT[task.priority]}>{task.priority}</Badge>
                <span className="text-body-sm text-foreground-faint">{task.due}</span>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </DashboardCard>
  );
}
