import type { ReactNode } from "react";

import { MobileSidebar, Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";
import { SidebarProvider } from "@/components/providers/sidebar-provider";
import { TooltipProvider } from "@/components/ui/tooltip";

/** Overall page chrome: sidebar + top bar + scrollable content region. */
export function AppShell({ children }: { children: ReactNode }) {
  return (
    <SidebarProvider>
      <TooltipProvider delayDuration={300}>
        <a
          href="#main-content"
          className="fixed left-4 top-4 z-toast -translate-y-24 border border-signal bg-ink px-4 py-2 text-body-sm text-signal transition-transform focus:translate-y-0"
        >
          Skip to content
        </a>
        <div className="flex h-screen flex-col">
          <div className="flex flex-1 overflow-hidden">
            <Sidebar />
            <MobileSidebar />
            <div className="flex flex-1 flex-col overflow-hidden">
              <Topbar />
              <main
                id="main-content"
                tabIndex={-1}
                className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-10"
              >
                {children}
              </main>
            </div>
          </div>
        </div>
      </TooltipProvider>
    </SidebarProvider>
  );
}
