import { Users } from "lucide-react";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/ui/empty-state";

export default function TeamWorkspacePage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-4xl">
        <PageHeader
          title="Team Workspace"
          description="Collaborate with your lab on shared papers and projects."
        />
        <EmptyState
          icon={Users}
          title="Not built yet"
          description="Shared workspaces are reserved here."
        />
      </div>
    </AppShell>
  );
}
