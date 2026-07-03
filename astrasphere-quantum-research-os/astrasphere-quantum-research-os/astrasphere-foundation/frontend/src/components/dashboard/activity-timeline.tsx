import { MessageCircle, Sparkles, Upload, UserPlus, type LucideIcon, Bookmark } from "lucide-react";

import { Panel } from "@/components/ui/panel";
import { RESEARCH_ACTIVITY, type ActivityEvent } from "@/data/mock";

const TYPE_ICON: Record<ActivityEvent["type"], LucideIcon> = {
  upload: Upload,
  comment: MessageCircle,
  save: Bookmark,
  ai: Sparkles,
  team: UserPlus,
};

const TYPE_COLOR: Record<ActivityEvent["type"], string> = {
  upload: "text-signal",
  comment: "text-entangled",
  save: "text-entangled",
  ai: "text-pulse",
  team: "text-signal",
};

/** Personal activity feed. Will source from GET /users/me/activity. */
export function ActivityTimeline() {
  return (
    <Panel>
      <h2 className="mb-5 font-display text-title text-foreground">Research Activity Timeline</h2>
      <ol className="relative space-y-5 border-l border-line pl-6">
        {RESEARCH_ACTIVITY.map((event) => {
          const Icon = TYPE_ICON[event.type];
          return (
            <li key={event.id} className="relative">
              <span
                className={`absolute -left-[29px] flex h-4 w-4 items-center justify-center rounded-full border border-line bg-ink-panel ${TYPE_COLOR[event.type]}`}
                aria-hidden
              >
                <Icon className="h-2.5 w-2.5" strokeWidth={2} />
              </span>
              <p className="text-body-sm text-foreground">{event.description}</p>
              <p className="mt-0.5 font-mono text-label text-foreground-faint">{event.timestamp}</p>
            </li>
          );
        })}
      </ol>
    </Panel>
  );
}
