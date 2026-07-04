import { AlertTriangle, CheckCircle2 } from "lucide-react";

import { cn } from "@/lib/utils";

/** Inline success/error banner for auth forms — one consistent shape
 * for every "invalid credentials" / "check your email" style message. */
export function FormMessage({
  variant,
  children,
}: {
  variant: "error" | "success";
  children: React.ReactNode;
}) {
  const Icon = variant === "error" ? AlertTriangle : CheckCircle2;
  return (
    <div
      role={variant === "error" ? "alert" : "status"}
      className={cn(
        "mb-4 flex items-start gap-2 border px-3 py-2.5 text-body-sm",
        variant === "error"
          ? "border-critical/30 bg-critical-subtle text-danger"
          : "border-success/30 bg-success-subtle text-signal-bright",
      )}
    >
      <Icon className="mt-0.5 h-4 w-4 shrink-0" aria-hidden />
      <span>{children}</span>
    </div>
  );
}
