"use client";

import { useContext } from "react";

import { SidebarContext } from "@/components/providers/sidebar-provider";

/** Access sidebar collapse/mobile-drawer state. Must be used within <SidebarProvider>. */
export function useSidebar() {
  const ctx = useContext(SidebarContext);
  if (!ctx) {
    throw new Error("useSidebar must be used within a SidebarProvider");
  }
  return ctx;
}
