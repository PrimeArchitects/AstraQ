import { Sigma } from "lucide-react";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/ui/empty-state";

export default function EquationExplorerPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-4xl">
        <PageHeader
          title="Equation Explorer"
          description="Look up and derive quantum formalism interactively."
        />
        <EmptyState
          icon={Sigma}
          title="Not built yet"
          description="An interactive equation workspace is reserved here."
        />
      </div>
    </AppShell>
  );
}
