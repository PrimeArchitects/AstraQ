import { AIInsightsCard } from "@/components/dashboard/ai-insights-card";
import { ActivityTimeline } from "@/components/dashboard/activity-timeline";
import { QuickActions } from "@/components/dashboard/quick-actions";
import { ReadingProgressCard } from "@/components/dashboard/reading-progress-card";
import { RecentConversationsCard } from "@/components/dashboard/recent-conversations-card";
import { RecentPapersCard } from "@/components/dashboard/recent-papers-card";
import { ResearchActivityCard } from "@/components/dashboard/research-activity-card";
import { SavedPapersCard } from "@/components/dashboard/saved-papers-card";
import { TrendingTopicsCard } from "@/components/dashboard/trending-topics-card";
import { UpcomingTasksCard } from "@/components/dashboard/upcoming-tasks-card";
import { AppShell } from "@/components/layout/app-shell";
import { CoherenceRing } from "@/components/layout/coherence-ring";
import { CURRENT_USER } from "@/data/mock";

export default function DashboardPage() {
  return (
    <AppShell>
      <div className="mx-auto flex max-w-7xl flex-col gap-8">
        <section className="flex flex-col items-start justify-between gap-6 border-b border-line pb-8 md:flex-row md:items-center">
          <div>
            <p className="font-mono text-label uppercase tracking-widest text-signal">
              Welcome back
            </p>
            <h1 className="mt-2 font-display text-display-md text-foreground">
              {CURRENT_USER.name.split(" ")[0]}&rsquo;s Research Console
            </h1>
            <p className="mt-2 max-w-md text-body-sm text-foreground-muted">{CURRENT_USER.role}</p>
          </div>
          <CoherenceRing className="h-24 w-24 shrink-0 md:h-28 md:w-28" />
        </section>

        <section>
          <h2 className="mb-3 font-mono text-label uppercase tracking-widest text-foreground-faint">
            Quick Actions
          </h2>
          <QuickActions />
        </section>

        <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          <div className="flex flex-col gap-4 lg:col-span-2">
            <RecentPapersCard />
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <TrendingTopicsCard />
              <SavedPapersCard />
            </div>
            <ResearchActivityCard />
          </div>
          <div className="flex flex-col gap-4">
            <ReadingProgressCard />
            <AIInsightsCard />
            <UpcomingTasksCard />
          </div>
        </section>

        <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          <div className="lg:col-span-1">
            <RecentConversationsCard />
          </div>
          <div className="lg:col-span-2">
            <ActivityTimeline />
          </div>
        </section>
      </div>
    </AppShell>
  );
}
