"use client";

import { Menu, Upload } from "lucide-react";

import { UploadPaperModal } from "@/components/dashboard/upload-paper-modal";
import { GlobalSearch } from "@/components/nav/global-search";
import { NotificationsMenu } from "@/components/nav/notifications-menu";
import { ThemeToggle } from "@/components/nav/theme-toggle";
import { UserMenu } from "@/components/nav/user-menu";
import { Button } from "@/components/ui/button";
import { siteConfig } from "@/config/site";
import { useSidebar } from "@/hooks/use-sidebar";

/** Fixed top bar: mobile nav trigger, search, and account/utility controls. */
export function Topbar() {
  const { setMobileOpen } = useSidebar();

  return (
    <header className="z-chrome flex h-14 shrink-0 items-center gap-3 border-b border-line bg-ink px-4 md:px-6">
      <button
        onClick={() => setMobileOpen(true)}
        aria-label="Open navigation"
        className="flex h-8 w-8 shrink-0 items-center justify-center rounded-control text-foreground-faint hover:bg-ink-raised hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal md:hidden"
      >
        <Menu className="h-4 w-4" aria-hidden />
      </button>

      <span className="font-display text-body-sm font-medium text-foreground md:hidden">
        {siteConfig.name}
      </span>

      <div className="flex-1">
        <GlobalSearch />
      </div>

      <div className="flex items-center gap-1.5">
        <UploadPaperModal
          trigger={
            <Button size="sm" className="hidden gap-1.5 sm:inline-flex">
              <Upload className="h-3.5 w-3.5" aria-hidden />
              Upload Paper
            </Button>
          }
        />
        <UploadPaperModal
          trigger={
            <Button
              size="sm"
              variant="ghost"
              className="h-8 w-8 p-0 sm:hidden"
              aria-label="Upload paper"
            >
              <Upload className="h-4 w-4" aria-hidden />
            </Button>
          }
        />
        <NotificationsMenu />
        <ThemeToggle />
        <UserMenu />
      </div>
    </header>
  );
}
