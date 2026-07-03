import { Newspaper } from "lucide-react";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/ui/empty-state";

export default function ResearchFeedPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-4xl">
        <PageHeader
          title="Research Feed"
          description="A curated feed of new papers matching your interests."
        />
        <EmptyState
          icon={Newspaper}
          title="Not built yet"
          description="Your personalized feed will appear here once topic subscriptions are implemented."
        />
      </div>
    </AppShell>
  );
}
