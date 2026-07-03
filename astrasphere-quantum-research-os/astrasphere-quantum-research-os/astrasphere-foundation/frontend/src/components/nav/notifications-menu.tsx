"use client";

import { Bell } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { NOTIFICATIONS } from "@/data/mock";

export function NotificationsMenu() {
  const unreadCount = NOTIFICATIONS.filter((n) => n.unread).length;

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="sm"
          className="relative h-8 w-8 p-0"
          aria-label={`Notifications${unreadCount > 0 ? `, ${unreadCount} unread` : ""}`}
        >
          <Bell className="h-4 w-4" aria-hidden />
          {unreadCount > 0 && (
            <span
              className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-signal"
              aria-hidden
            />
          )}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-80">
        <DropdownMenuLabel>Notifications</DropdownMenuLabel>
        <DropdownMenuSeparator />
        {NOTIFICATIONS.map((n) => (
          <DropdownMenuItem key={n.id} className="flex-col items-start gap-0.5">
            <span className="flex w-full items-center gap-2 text-foreground">
              {n.unread && (
                <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-signal" aria-hidden />
              )}
              <span className={n.unread ? "" : "ml-3.5"}>{n.title}</span>
            </span>
            <span className="ml-3.5 font-mono text-label text-foreground-faint">{n.time}</span>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
