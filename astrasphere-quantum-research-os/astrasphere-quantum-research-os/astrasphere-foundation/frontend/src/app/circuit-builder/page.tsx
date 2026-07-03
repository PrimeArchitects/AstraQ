import { CircuitBoard } from "lucide-react";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/ui/empty-state";

export default function CircuitBuilderPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-4xl">
        <PageHeader
          title="Circuit Builder"
          description="Sketch and simulate quantum circuits visually."
        />
        <EmptyState
          icon={CircuitBoard}
          title="Not built yet"
          description="A drag-and-drop circuit canvas is reserved here."
        />
      </div>
    </AppShell>
  );
}
