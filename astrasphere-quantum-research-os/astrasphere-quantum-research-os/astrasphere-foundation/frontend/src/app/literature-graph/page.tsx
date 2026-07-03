import { Network } from "lucide-react";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/ui/empty-state";

export default function LiteratureGraphPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-4xl">
        <PageHeader
          title="Literature Graph"
          description="Explore how papers in your library connect through citations."
        />
        <EmptyState
          icon={Network}
          title="Not built yet"
          description="A citation graph visualization is reserved here."
        />
      </div>
    </AppShell>
  );
}
