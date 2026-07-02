import type { HTMLAttributes, ReactNode } from "react";

import { cn } from "@/lib/utils";

/**
 * Instrument-panel container — the app's signature framing device.
 * Corner brackets echo an oscilloscope bezel; every data surface in the
 * console sits inside one of these rather than a plain rounded card.
 */
export function Panel({ className, children, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("relative border border-line bg-ink-panel/60 p-5 backdrop-blur-sm", className)}
      {...props}
    >
      <span className="absolute left-0 top-0 h-3 w-3 border-l border-t border-signal/50" />
      <span className="absolute right-0 top-0 h-3 w-3 border-r border-t border-signal/50" />
      <span className="absolute bottom-0 left-0 h-3 w-3 border-b border-l border-signal/50" />
      <span className="absolute bottom-0 right-0 h-3 w-3 border-b border-r border-signal/50" />
      {children}
    </div>
  );
}

export function PanelLabel({ children }: { children: ReactNode }) {
  return (
    <p className="mb-3 font-mono text-[11px] uppercase tracking-[0.2em] text-foreground-faint">
      {children}
    </p>
  );
}
