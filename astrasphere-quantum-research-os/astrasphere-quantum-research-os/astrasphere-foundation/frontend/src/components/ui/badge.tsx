import { cva, type VariantProps } from "class-variance-authority";
import type { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-pill border px-2 py-0.5 font-mono text-label uppercase tracking-widest",
  {
    variants: {
      variant: {
        neutral: "border-line bg-ink-raised text-foreground-muted",
        success: "border-success/30 bg-success-subtle text-signal-bright",
        warning: "border-warning/30 bg-warning-subtle text-pulse",
        info: "border-info/30 bg-info-subtle text-entangled",
        critical: "border-critical/30 bg-critical-subtle text-danger",
      },
    },
    defaultVariants: { variant: "neutral" },
  },
);

export interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

/** Small status pill — used for paper status, task priority, subsystem health, etc. */
export function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant, className }))} {...props} />;
}
