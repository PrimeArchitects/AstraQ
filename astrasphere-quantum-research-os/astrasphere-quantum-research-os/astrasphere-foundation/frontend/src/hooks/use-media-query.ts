"use client";

import { useEffect, useState } from "react";

/**
 * Tracks a CSS media query in React state. Used for behavior that can't
 * be expressed in Tailwind alone (e.g. switching the sidebar from an
 * inline column to an overlay drawer below the `md` breakpoint).
 *
 * Returns `false` on the server and during initial hydration to avoid
 * a mismatch; the real value settles on mount.
 */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mediaQueryList = window.matchMedia(query);
    setMatches(mediaQueryList.matches);

    const listener = (event: MediaQueryListEvent) => setMatches(event.matches);
    mediaQueryList.addEventListener("change", listener);
    return () => mediaQueryList.removeEventListener("change", listener);
  }, [query]);

  return matches;
}
