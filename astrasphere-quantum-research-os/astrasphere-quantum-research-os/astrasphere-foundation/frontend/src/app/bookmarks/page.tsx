import { Bookmark } from "lucide-react";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/ui/empty-state";
import { Panel } from "@/components/ui/panel";
import { SAVED_PAPERS } from "@/data/mock";

export default function BookmarksPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-4xl">
        <PageHeader title="Bookmarks" description="Papers you've saved for later reading." />
        {SAVED_PAPERS.length === 0 ? (
          <EmptyState
            icon={Bookmark}
            title="No bookmarks yet"
            description="Save a paper from My Papers or the Research Feed to see it here."
          />
        ) : (
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {SAVED_PAPERS.map((paper) => (
              <Panel key={paper.id}>
                <div className="flex items-start gap-2.5">
                  <Bookmark className="mt-0.5 h-4 w-4 shrink-0 text-entangled" aria-hidden />
                  <div className="min-w-0">
                    <p className="text-body-sm font-medium text-foreground">{paper.title}</p>
                    <p className="mt-1 text-body-sm text-foreground-faint">
                      {paper.authors.join(", ")} &middot; {paper.year}
                    </p>
                  </div>
                </div>
              </Panel>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
}
