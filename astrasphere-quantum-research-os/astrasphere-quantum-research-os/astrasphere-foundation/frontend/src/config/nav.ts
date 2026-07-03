import type { LucideIcon } from "lucide-react";
import {
  Bookmark,
  CircuitBoard,
  Columns3,
  FlaskConical,
  LayoutDashboard,
  MessageSquareText,
  Network,
  Newspaper,
  Settings as SettingsIcon,
  Sigma,
  SquareStack,
  Users,
} from "lucide-react";
import type { Route } from "next";

export interface NavItem {
  label: string;
  href: Route;
  icon: LucideIcon;
  /** Shown as a small pill next to the label (e.g. unread counts). Mock-only for now. */
  badge?: number;
}

/**
 * Primary sidebar navigation. Order here is the order rendered — group
 * boundaries below are visual only (see Sidebar component) and don't
 * affect routing.
 */
export const primaryNav: NavItem[] = [
  { label: "Dashboard", href: "/", icon: LayoutDashboard },
  { label: "Research Feed", href: "/research-feed", icon: Newspaper, badge: 12 },
  { label: "My Papers", href: "/my-papers", icon: SquareStack },
  { label: "AI Assistant", href: "/ai-assistant", icon: MessageSquareText },
];

export const toolsNav: NavItem[] = [
  { label: "Equation Explorer", href: "/equation-explorer", icon: Sigma },
  { label: "Circuit Builder", href: "/circuit-builder", icon: CircuitBoard },
  { label: "Literature Graph", href: "/literature-graph", icon: Network },
  { label: "Paper Comparison", href: "/paper-comparison", icon: Columns3 },
  { label: "Experiment Designer", href: "/experiment-designer", icon: FlaskConical },
];

export const workspaceNav: NavItem[] = [
  { label: "Team Workspace", href: "/team-workspace", icon: Users },
  { label: "Bookmarks", href: "/bookmarks", icon: Bookmark },
];

export const footerNav: NavItem[] = [{ label: "Settings", href: "/settings", icon: SettingsIcon }];

export const allNav: NavItem[] = [...primaryNav, ...toolsNav, ...workspaceNav, ...footerNav];
