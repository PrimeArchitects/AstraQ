import type { ReactNode } from "react";

import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";

/** Overall page chrome: top bar + sidebar + scrollable content region. */
export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen flex-col">
      <Topbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-6 md:p-10">{children}</main>
      </div>
    </div>
  );
}
