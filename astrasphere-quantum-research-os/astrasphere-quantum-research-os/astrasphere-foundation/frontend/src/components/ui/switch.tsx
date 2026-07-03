"use client";

import * as SwitchPrimitive from "@radix-ui/react-switch";
import type { ComponentPropsWithoutRef, ElementRef } from "react";
import { forwardRef } from "react";

import { cn } from "@/lib/utils";

export const Switch = forwardRef<
  ElementRef<typeof SwitchPrimitive.Root>,
  ComponentPropsWithoutRef<typeof SwitchPrimitive.Root>
>(({ className, ...props }, ref) => (
  <SwitchPrimitive.Root
    ref={ref}
    className={cn(
      "relative h-5 w-9 shrink-0 rounded-pill border border-line bg-ink-raised transition-colors",
      "data-[state=checked]:border-signal data-[state=checked]:bg-signal/30",
      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal",
      className,
    )}
    {...props}
  >
    <SwitchPrimitive.Thumb className="block h-3.5 w-3.5 translate-x-0.5 rounded-full bg-foreground-faint transition-transform data-[state=checked]:translate-x-[18px] data-[state=checked]:bg-signal" />
  </SwitchPrimitive.Root>
));
Switch.displayName = "Switch";

export function SwitchRow({
  id,
  label,
  description,
  ...props
}: ComponentPropsWithoutRef<typeof SwitchPrimitive.Root> & {
  id: string;
  label: string;
  description?: string;
}) {
  return (
    <div className="flex items-center justify-between gap-4 py-3">
      <div>
        <label htmlFor={id} className="text-body-sm text-foreground">
          {label}
        </label>
        {description && <p className="mt-0.5 text-body-sm text-foreground-faint">{description}</p>}
      </div>
      <Switch id={id} {...props} />
    </div>
  );
}
