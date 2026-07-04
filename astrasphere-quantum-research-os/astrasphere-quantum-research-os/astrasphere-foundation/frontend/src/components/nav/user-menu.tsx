"use client";

import { LogOut, Settings, User } from "lucide-react";
import { signOut } from "next-auth/react";
import Link from "next/link";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useCurrentUser } from "@/hooks/use-current-user";
import { apiClient } from "@/lib/api-client";

function initials(name: string): string {
  return name
    .split(" ")
    .map((p) => p[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

async function handleSignOut() {
  // Revoke the backend session first (its cookies are what actually
  // authenticate API calls); Auth.js's signOut() then clears the
  // frontend session cookie and redirects.
  try {
    await apiClient.post("/auth/logout");
  } catch {
    // Backend session may already be expired — still proceed to clear
    // the frontend session either way.
  }
  await signOut({ callbackUrl: "/login" });
}

export function UserMenu() {
  const { user } = useCurrentUser();
  if (!user) return null;

  const displayName = user.name ?? user.email ?? "Account";

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button
          className="rounded-panel focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal"
          aria-label="Open account menu"
        >
          <Avatar>
            <AvatarFallback>{initials(displayName)}</AvatarFallback>
          </Avatar>
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel className="normal-case tracking-normal">
          <p className="text-body-sm font-medium text-foreground">{displayName}</p>
          <p className="text-body-sm text-foreground-faint">{user.email}</p>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem asChild>
          <Link href="/profile">
            <User className="h-4 w-4" aria-hidden /> Profile
          </Link>
        </DropdownMenuItem>
        <DropdownMenuItem asChild>
          <Link href="/settings">
            <Settings className="h-4 w-4" aria-hidden /> Settings
          </Link>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          className="text-danger data-[highlighted]:text-danger"
          onSelect={handleSignOut}
        >
          <LogOut className="h-4 w-4" aria-hidden /> Sign out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
