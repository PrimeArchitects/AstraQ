import { Columns3 } from "lucide-react";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/ui/empty-state";

export default function PaperComparisonPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-4xl">
        <PageHeader
          title="Paper Comparison"
          description="Compare methods, results, and claims across papers side by side."
        />
        <EmptyState
          icon={Columns3}
          title="Not built yet"
          description="Select papers from My Papers to compare once this tool is built."
        />
      </div>
    </AppShell>
  );
}
