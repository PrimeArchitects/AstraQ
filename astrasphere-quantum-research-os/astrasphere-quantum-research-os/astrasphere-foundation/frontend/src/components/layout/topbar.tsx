import { StatusDot } from "@/components/ui/status-dot";
import { siteConfig } from "@/config/site";

/** Fixed top bar: product identity + live system status readout. */
export function Topbar() {
  return (
    <header className="flex h-14 shrink-0 items-center justify-between border-b border-line bg-ink px-6">
      <div className="flex items-center gap-3">
        <div className="h-2 w-2 rotate-45 border border-signal" aria-hidden />
        <span className="font-display text-sm font-medium tracking-wide text-foreground">
          {siteConfig.name}
        </span>
        <span className="font-mono text-[11px] text-foreground-faint">/ RESEARCH OS</span>
      </div>
      <div className="flex items-center gap-4 font-mono text-[11px] text-foreground-muted">
        <span className="flex items-center gap-2">
          <StatusDot status="nominal" />
          SYSTEMS NOMINAL
        </span>
        <span className="text-foreground-faint">v0.1.0-foundation</span>
      </div>
    </header>
  );
}
