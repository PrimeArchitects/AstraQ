import { cn } from "@/lib/utils";
import type { SystemStatus } from "@/types";

const STATUS_STYLES: Record<SystemStatus, string> = {
  nominal: "bg-signal shadow-[0_0_8px_theme(colors.signal.DEFAULT)]",
  degraded: "bg-pulse shadow-[0_0_8px_theme(colors.pulse.DEFAULT)]",
  offline: "bg-danger shadow-[0_0_8px_theme(colors.danger.DEFAULT)]",
};

/** Small LED-style indicator used throughout the console for live status. */
export function StatusDot({ status }: { status: SystemStatus }) {
  return (
    <span className="inline-flex items-center gap-2">
      <span className={cn("h-1.5 w-1.5 rounded-full", STATUS_STYLES[status])} />
    </span>
  );
}
