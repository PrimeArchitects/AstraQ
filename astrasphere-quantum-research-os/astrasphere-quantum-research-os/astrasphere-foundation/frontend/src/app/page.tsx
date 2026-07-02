import { AppShell } from "@/components/layout/app-shell";
import { CoherenceRing } from "@/components/layout/coherence-ring";
import { Panel, PanelLabel } from "@/components/ui/panel";
import { StatusDot } from "@/components/ui/status-dot";

const READOUTS = [
  { label: "Active Experiments", value: "00", unit: "running" },
  { label: "Compute Queue", value: "00", unit: "jobs" },
  { label: "Datasets Indexed", value: "00", unit: "sets" },
] as const;

const SUBSYSTEMS = [
  { name: "API Gateway", status: "nominal" as const },
  { name: "Postgres", status: "nominal" as const },
  { name: "Redis Cache", status: "nominal" as const },
  { name: "Vector Store", status: "nominal" as const },
  { name: "AI Provider", status: "degraded" as const },
];

export default function DashboardPage() {
  return (
    <AppShell>
      <div className="mx-auto flex max-w-6xl flex-col gap-10">
        <section className="flex flex-col items-start justify-between gap-8 border-b border-line pb-10 md:flex-row md:items-center">
          <div>
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-signal">
              Foundation Build
            </p>
            <h1 className="mt-3 max-w-xl font-display text-3xl font-medium leading-tight text-foreground md:text-4xl">
              AstraSphere Quantum Research OS
            </h1>
            <p className="mt-4 max-w-md text-sm leading-relaxed text-foreground-muted">
              The console shell is online. Experiment tracking, datasets, and AI-assisted analysis
              attach to this scaffold in later phases.
            </p>
          </div>
          <CoherenceRing />
        </section>

        <section className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          {READOUTS.map((r) => (
            <Panel key={r.label}>
              <PanelLabel>{r.label}</PanelLabel>
              <p className="font-mono text-3xl text-foreground">
                {r.value}
                <span className="ml-2 text-sm text-foreground-faint">{r.unit}</span>
              </p>
            </Panel>
          ))}
        </section>

        <section>
          <Panel>
            <PanelLabel>Subsystem Status</PanelLabel>
            <ul className="divide-y divide-line-faint">
              {SUBSYSTEMS.map((s) => (
                <li
                  key={s.name}
                  className="flex items-center justify-between py-3 first:pt-0 last:pb-0"
                >
                  <span className="text-sm text-foreground">{s.name}</span>
                  <span className="flex items-center gap-2 font-mono text-[11px] uppercase text-foreground-muted">
                    <StatusDot status={s.status} />
                    {s.status}
                  </span>
                </li>
              ))}
            </ul>
          </Panel>
        </section>

        <section className="border border-dashed border-line p-6 text-center">
          <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-foreground-faint">
            Extension Point
          </p>
          <p className="mx-auto mt-2 max-w-md text-sm text-foreground-muted">
            This panel marks where experiment workspaces, live job monitors, and AI research
            copilots will mount once those features are built.
          </p>
        </section>
      </div>
    </AppShell>
  );
}
