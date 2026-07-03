import { cn } from "@/lib/utils";

export interface ProgressProps {
  /** 0–100 */
  value: number;
  label?: string;
  className?: string;
  /** Accessible label for screen readers when `label` isn't visually descriptive enough. */
  "aria-label"?: string;
}

/** Linear progress bar. Used for reading progress, task completion, upload status. */
export function Progress({ value, label, className, "aria-label": ariaLabel }: ProgressProps) {
  const clamped = Math.min(100, Math.max(0, value));
  return (
    <div className={cn("w-full", className)}>
      {label && (
        <div className="mb-1.5 flex items-center justify-between font-mono text-label uppercase tracking-widest text-foreground-faint">
          <span>{label}</span>
          <span>{clamped}%</span>
        </div>
      )}
      <div
        role="progressbar"
        aria-valuenow={clamped}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={ariaLabel ?? label}
        className="h-1.5 w-full overflow-hidden rounded-pill bg-ink-raised"
      >
        <div
          className="h-full rounded-pill bg-signal transition-[width] duration-500 ease-out"
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  );
}
