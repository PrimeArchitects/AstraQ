"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { Badge } from "@/components/ui/badge";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import type { NavItem } from "@/config/nav";
import { cn } from "@/lib/utils";

/**
 * Renders one group of sidebar links. Active state is derived from the
 * current pathname (exact match for "/", prefix match otherwise) rather
 * than passed in, so it always reflects real navigation state.
 */
export function NavSection({
  items,
  label,
  collapsed,
  onNavigate,
}: {
  items: NavItem[];
  label?: string;
  collapsed: boolean;
  onNavigate?: () => void;
}) {
  const pathname = usePathname();

  return (
    <div>
      {label && !collapsed && (
        <p className="mb-2 px-3 font-mono text-label uppercase tracking-widest text-foreground-faint">
          {label}
        </p>
      )}
      <ul className="space-y-0.5">
        {items.map((item) => {
          const isActive = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
          const Icon = item.icon;

          const link = (
            <Link
              href={item.href}
              onClick={onNavigate}
              aria-current={isActive ? "page" : undefined}
              className={cn(
                "group flex items-center gap-3 rounded-control px-3 py-2 text-body-sm transition-colors",
                collapsed && "justify-center px-0",
                isActive
                  ? "bg-ink-raised text-signal"
                  : "text-foreground-muted hover:bg-ink-raised hover:text-foreground",
              )}
            >
              <Icon
                className={cn(
                  "h-4 w-4 shrink-0",
                  isActive ? "text-signal" : "text-foreground-faint group-hover:text-foreground",
                )}
                strokeWidth={1.75}
                aria-hidden
              />
              {!collapsed && (
                <>
                  <span className="flex-1 truncate">{item.label}</span>
                  {item.badge !== undefined && (
                    <Badge variant="info" className="px-1.5">
                      {item.badge}
                    </Badge>
                  )}
                </>
              )}
            </Link>
          );

          if (!collapsed) return <li key={item.href}>{link}</li>;

          return (
            <li key={item.href}>
              <Tooltip>
                <TooltipTrigger asChild>{link}</TooltipTrigger>
                <TooltipContent side="right">{item.label}</TooltipContent>
              </Tooltip>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
