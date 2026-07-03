"use client";

import * as DialogPrimitive from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import type { ComponentPropsWithoutRef, ReactNode } from "react";

import { cn } from "@/lib/utils";

export const Modal = DialogPrimitive.Root;
export const ModalTrigger = DialogPrimitive.Trigger;
export const ModalClose = DialogPrimitive.Close;

/**
 * Accessible modal dialog (built on Radix Dialog: focus trap, Escape to
 * close, click-outside to close, `role="dialog"` + `aria-modal` wired
 * automatically). Use for confirmations and short focused forms — not
 * for full page-replacement flows.
 */
export function ModalContent({
  title,
  description,
  children,
  className,
  ...props
}: ComponentPropsWithoutRef<typeof DialogPrimitive.Content> & {
  title: string;
  description?: string;
  children?: ReactNode;
}) {
  return (
    <DialogPrimitive.Portal>
      <DialogPrimitive.Overlay className="fixed inset-0 z-overlay animate-overlay-in bg-ink-overlay/80" />
      <DialogPrimitive.Content
        className={cn(
          "fixed left-1/2 top-1/2 z-modal w-full max-w-md -translate-x-1/2 -translate-y-1/2",
          "animate-dialog-in border border-line bg-ink-panel p-6 shadow-raised",
          "focus:outline-none",
          className,
        )}
        {...props}
      >
        <div className="mb-4 flex items-start justify-between gap-4">
          <div>
            <DialogPrimitive.Title className="font-display text-title text-foreground">
              {title}
            </DialogPrimitive.Title>
            {description && (
              <DialogPrimitive.Description className="mt-1 text-body-sm text-foreground-muted">
                {description}
              </DialogPrimitive.Description>
            )}
          </div>
          <DialogPrimitive.Close
            className="shrink-0 rounded-control p-1 text-foreground-faint transition-colors hover:bg-ink-raised hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal"
            aria-label="Close dialog"
          >
            <X className="h-4 w-4" aria-hidden />
          </DialogPrimitive.Close>
        </div>
        {children}
      </DialogPrimitive.Content>
    </DialogPrimitive.Portal>
  );
}
