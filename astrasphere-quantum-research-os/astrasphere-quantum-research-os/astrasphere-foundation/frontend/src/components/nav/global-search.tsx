"use client";

import { Search } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

/**
 * Global search input. Not wired to a real search backend yet — Cmd/Ctrl+K
 * focuses it, which is the interaction contract a future search
 * implementation should preserve.
 */
export function GlobalSearch() {
  const [value, setValue] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    function handleKeydown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        inputRef.current?.focus();
      }
    }
    window.addEventListener("keydown", handleKeydown);
    return () => window.removeEventListener("keydown", handleKeydown);
  }, []);

  return (
    <div className="relative hidden w-full max-w-sm sm:block">
      <Search
        className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-foreground-faint"
        aria-hidden
      />
      <Input
        ref={inputRef}
        type="search"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Search papers, equations, conversations..."
        aria-label="Global search"
        className="h-8 pl-8 pr-14 text-body-sm"
      />
      <kbd
        className={cn(
          "pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 rounded border border-line px-1.5 py-0.5 font-mono text-[10px] text-foreground-faint",
        )}
      >
        ⌘K
      </kbd>
    </div>
  );
}
