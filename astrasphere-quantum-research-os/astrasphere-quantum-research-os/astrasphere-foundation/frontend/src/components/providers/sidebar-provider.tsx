"use client";

import { createContext, useCallback, useEffect, useState, type ReactNode } from "react";

const STORAGE_KEY = "astrasphere:sidebar-collapsed";

interface SidebarContextValue {
  /** Desktop: whether the sidebar is collapsed to icon-only width. */
  collapsed: boolean;
  toggleCollapsed: () => void;
  /** Mobile: whether the drawer overlay is open. */
  mobileOpen: boolean;
  setMobileOpen: (open: boolean) => void;
}

export const SidebarContext = createContext<SidebarContextValue | null>(null);

/**
 * Owns sidebar layout state for the whole app. Desktop collapse state
 * persists across sessions (a genuine preference); mobile drawer state
 * is always session-local and closes on every route change.
 */
export function SidebarProvider({ children }: { children: ReactNode }) {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (stored === "true") setCollapsed(true);
  }, []);

  const toggleCollapsed = useCallback(() => {
    setCollapsed((prev) => {
      const next = !prev;
      window.localStorage.setItem(STORAGE_KEY, String(next));
      return next;
    });
  }, []);

  return (
    <SidebarContext.Provider value={{ collapsed, toggleCollapsed, mobileOpen, setMobileOpen }}>
      {children}
    </SidebarContext.Provider>
  );
}
