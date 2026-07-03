"use client";

import * as DialogPrimitive from "@radix-ui/react-dialog";
import { PanelLeftClose, PanelLeftOpen, X } from "lucide-react";
import Link from "next/link";

import { NavSection } from "@/components/layout/nav-section";
import { footerNav, primaryNav, toolsNav, workspaceNav } from "@/config/nav";
import { siteConfig } from "@/config/site";
import { useSidebar } from "@/hooks/use-sidebar";
import { cn } from "@/lib/utils";

function SidebarContents({
  collapsed,
  onNavigate,
}: {
  collapsed: boolean;
  onNavigate?: () => void;
}) {
  return (
    <div className="flex h-full flex-col gap-6 overflow-y-auto px-3 py-5">
      <NavSection items={primaryNav} collapsed={collapsed} onNavigate={onNavigate} />
      <NavSection items={toolsNav} label="Tools" collapsed={collapsed} onNavigate={onNavigate} />
      <NavSection
        items={workspaceNav}
        label="Workspace"
        collapsed={collapsed}
        onNavigate={onNavigate}
      />
      <div className="mt-auto">
        <NavSection items={footerNav} collapsed={collapsed} onNavigate={onNavigate} />
      </div>
    </div>
  );
}

/** Desktop sidebar (md+): collapsible column, persists collapse state. */
export function Sidebar() {
  const { collapsed, toggleCollapsed } = useSidebar();

  return (
    <nav
      aria-label="Primary"
      className={cn(
        "hidden shrink-0 flex-col border-r border-line bg-ink transition-[width] duration-200 md:flex",
        collapsed ? "w-16" : "w-64",
      )}
    >
      <div className="flex h-14 shrink-0 items-center justify-between border-b border-line px-3">
        {!collapsed && (
          <Link href="/" className="flex items-center gap-2 overflow-hidden">
            <div className="h-2 w-2 shrink-0 rotate-45 border border-signal" aria-hidden />
            <span className="truncate font-display text-body-sm font-medium text-foreground">
              {siteConfig.name}
            </span>
          </Link>
        )}
        <button
          onClick={toggleCollapsed}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          className={cn(
            "flex h-8 w-8 shrink-0 items-center justify-center rounded-control text-foreground-faint transition-colors hover:bg-ink-raised hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal",
            collapsed && "mx-auto",
          )}
        >
          {collapsed ? (
            <PanelLeftOpen className="h-4 w-4" aria-hidden />
          ) : (
            <PanelLeftClose className="h-4 w-4" aria-hidden />
          )}
        </button>
      </div>
      <SidebarContents collapsed={collapsed} />
    </nav>
  );
}

/** Mobile navigation (below md): full drawer overlay, built on Radix Dialog for a11y. */
export function MobileSidebar() {
  const { mobileOpen, setMobileOpen } = useSidebar();

  return (
    <DialogPrimitive.Root open={mobileOpen} onOpenChange={setMobileOpen}>
      <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay className="fixed inset-0 z-overlay animate-overlay-in bg-ink-overlay/80 md:hidden" />
        <DialogPrimitive.Content
          className="fixed inset-y-0 left-0 z-modal w-72 animate-slide-in-left border-r border-line bg-ink focus:outline-none md:hidden"
          aria-describedby={undefined}
        >
          <DialogPrimitive.Title className="sr-only">Navigation</DialogPrimitive.Title>
          <div className="flex h-14 shrink-0 items-center justify-between border-b border-line px-4">
            <Link href="/" onClick={() => setMobileOpen(false)} className="flex items-center gap-2">
              <div className="h-2 w-2 rotate-45 border border-signal" aria-hidden />
              <span className="font-display text-body-sm font-medium text-foreground">
                {siteConfig.name}
              </span>
            </Link>
            <DialogPrimitive.Close
              aria-label="Close navigation"
              className="flex h-8 w-8 items-center justify-center rounded-control text-foreground-faint hover:bg-ink-raised hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal"
            >
              <X className="h-4 w-4" aria-hidden />
            </DialogPrimitive.Close>
          </div>
          <SidebarContents collapsed={false} onNavigate={() => setMobileOpen(false)} />
        </DialogPrimitive.Content>
      </DialogPrimitive.Portal>
    </DialogPrimitive.Root>
  );
}
