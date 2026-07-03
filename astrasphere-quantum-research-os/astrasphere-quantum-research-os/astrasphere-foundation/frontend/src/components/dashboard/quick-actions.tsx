import {
  CircuitBoard,
  Columns3,
  MessageSquareText,
  Network,
  Sigma,
  Upload,
  type LucideIcon,
} from "lucide-react";
import type { Route } from "next";
import Link from "next/link";

import { UploadPaperModal } from "@/components/dashboard/upload-paper-modal";
import { Panel } from "@/components/ui/panel";
import { QUICK_ACTIONS, type QuickAction } from "@/data/mock";

const ICONS: Record<string, LucideIcon> = {
  qa1: Upload,
  qa2: Columns3,
  qa3: MessageSquareText,
  qa4: Sigma,
  qa5: CircuitBoard,
  qa6: Network,
};

function ActionCardBody({ action, Icon }: { action: QuickAction; Icon: LucideIcon }) {
  return (
    <Panel className="flex h-full flex-col gap-3 transition-colors hover:border-signal/40">
      <Icon className="h-5 w-5 text-signal" strokeWidth={1.75} aria-hidden />
      <div>
        <p className="text-body-sm font-medium text-foreground">{action.title}</p>
        <p className="mt-1 text-body-sm text-foreground-muted">{action.description}</p>
      </div>
    </Panel>
  );
}

/** Grid of primary actions. "Upload Research Paper" opens a modal; the rest deep-link to their tool. */
export function QuickActions() {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
      {QUICK_ACTIONS.map((action) => {
        const Icon = ICONS[action.id] ?? Upload;

        if (!action.href) {
          return (
            <UploadPaperModal
              key={action.id}
              trigger={
                <button className="text-left" aria-label={action.title}>
                  <ActionCardBody action={action} Icon={Icon} />
                </button>
              }
            />
          );
        }

        return (
          <Link key={action.id} href={action.href as Route} className="block">
            <ActionCardBody action={action} Icon={Icon} />
          </Link>
        );
      })}
    </div>
  );
}
