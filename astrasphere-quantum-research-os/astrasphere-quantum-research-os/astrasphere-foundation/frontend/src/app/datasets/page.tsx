import { AppShell } from "@/components/layout/app-shell";
import { Panel, PanelLabel } from "@/components/ui/panel";

/**
 * Placeholder route — reserved for the datasets feature domain.
 * Intentionally unimplemented in the foundation phase; wire up real
 * data fetching and UI here once that feature is built.
 */
export default function DatasetsPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-6xl">
        <Panel>
          <PanelLabel>Datasets</PanelLabel>
          <p className="text-sm text-foreground-muted">
            This module is not yet implemented. It is reserved as an extension point for the
            datasets feature domain.
          </p>
        </Panel>
      </div>
    </AppShell>
  );
}
