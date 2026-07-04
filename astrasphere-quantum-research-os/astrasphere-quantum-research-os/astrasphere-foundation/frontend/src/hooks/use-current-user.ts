"use client";

import { useSession } from "next-auth/react";

/** Thin, typed wrapper over Auth.js's useSession — the one place that
 * knows the session shape, so components don't import next-auth directly. */
export function useCurrentUser() {
  const { data: session, status } = useSession();
  return {
    user: session?.user ?? null,
    isLoading: status === "loading",
    isAuthenticated: status === "authenticated",
  };
}
