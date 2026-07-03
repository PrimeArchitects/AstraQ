import { MessageSquareText } from "lucide-react";

import { DashboardCard } from "@/components/dashboard/dashboard-card";
import { EmptyState } from "@/components/ui/empty-state";
import { RECENT_CONVERSATIONS } from "@/data/mock";

/** Recent AI Assistant threads. Will source from GET /ai/conversations?sort=recent. */
export function RecentConversationsCard() {
  if (RECENT_CONVERSATIONS.length === 0) {
    return (
      <DashboardCard title="Recent Conversations">
        <EmptyState
          icon={MessageSquareText}
          title="No conversations yet"
          description="Ask the AI Assistant a question to get started."
        />
      </DashboardCard>
    );
  }

  return (
    <DashboardCard
      title="Recent Conversations"
      action={{ label: "Open assistant", href: "/ai-assistant" }}
    >
      <ul className="divide-y divide-line-faint">
        {RECENT_CONVERSATIONS.map((c) => (
          <li key={c.id} className="py-3 first:pt-0 last:pb-0">
            <div className="flex items-center justify-between gap-3">
              <p className="truncate text-body-sm font-medium text-foreground">{c.title}</p>
              <span className="shrink-0 font-mono text-label text-foreground-faint">
                {c.updatedAt}
              </span>
            </div>
            <p className="mt-1 line-clamp-1 text-body-sm text-foreground-muted">{c.lastMessage}</p>
          </li>
        ))}
      </ul>
    </DashboardCard>
  );
}
