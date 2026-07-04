import Link from "next/link";

import { CoherenceRing } from "@/components/layout/coherence-ring";
import { siteConfig } from "@/config/site";

/**
 * Dedicated chrome for login/signup/password-flow pages — deliberately
 * without the app shell's sidebar/top bar, since none of that applies
 * before a session exists.
 */
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-ink px-4 py-12">
      <Link href="/" className="mb-8 flex items-center gap-2">
        <div className="h-2.5 w-2.5 rotate-45 border border-signal" aria-hidden />
        <span className="font-display text-body font-medium text-foreground">
          {siteConfig.fullName}
        </span>
      </Link>
      <div className="w-full max-w-sm">{children}</div>
      <CoherenceRing className="pointer-events-none absolute bottom-[-4rem] right-[-4rem] h-56 w-56 opacity-20 md:opacity-30" />
    </div>
  );
}
