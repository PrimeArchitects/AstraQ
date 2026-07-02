import Link from "next/link";

import { siteConfig } from "@/config/site";

/** Primary navigation. Feature-first routes get added here as they ship. */
export function Sidebar() {
  return (
    <nav className="hidden w-56 shrink-0 border-r border-line bg-ink px-3 py-6 md:block">
      <ul className="space-y-1">
        {siteConfig.nav.map((item) => (
          <li key={item.href}>
            <Link
              href={item.href}
              className="block px-3 py-2 font-mono text-[13px] text-foreground-muted transition-colors hover:bg-ink-raised hover:text-foreground"
            >
              {item.label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
