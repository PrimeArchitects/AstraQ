import { FlaskConical } from "lucide-react";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/ui/empty-state";

export default function ExperimentDesignerPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-4xl">
        <PageHeader
          title="Experiment Designer"
          description="Plan and structure quantum experiments before running them."
        />
        <EmptyState
          icon={FlaskConical}
          title="Not built yet"
          description="A guided experiment-design workflow is reserved here."
        />
      </div>
    </AppShell>
  );
}
