import { AppShell } from "@/components/layout/app-shell";
import { Panel, PanelLabel } from "@/components/ui/panel";

/**
 * Placeholder route — reserved for the experiments feature domain.
 * Intentionally unimplemented in the foundation phase; wire up real
 * data fetching and UI here once that feature is built.
 */
export default function ExperimentsPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-6xl">
        <Panel>
          <PanelLabel>Experiments</PanelLabel>
          <p className="text-sm text-foreground-muted">
            This module is not yet implemented. It is reserved as an extension point for the
            experiments feature domain.
          </p>
        </Panel>
      </div>
    </AppShell>
  );
}
