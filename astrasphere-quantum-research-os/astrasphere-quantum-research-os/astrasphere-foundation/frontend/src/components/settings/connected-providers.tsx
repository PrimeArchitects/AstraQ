"use client";

import { KeyRound } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuthProviders } from "@/hooks/use-profile";

const PROVIDER_LABELS: Record<string, string> = {
  password: "Email & password",
  google: "Google",
};

export function ConnectedProviders() {
  const { data: providers, isLoading } = useAuthProviders();

  if (isLoading) return <Skeleton className="h-16" />;

  return (
    <ul className="divide-y divide-line-faint">
      {providers?.map((p) => (
        <li key={p.provider} className="flex items-center justify-between py-2.5">
          <span className="flex items-center gap-2 text-body-sm text-foreground">
            <KeyRound className="h-3.5 w-3.5 text-foreground-faint" aria-hidden />
            {PROVIDER_LABELS[p.provider] ?? p.provider}
          </span>
          <Badge variant="success">Connected</Badge>
        </li>
      ))}
    </ul>
  );
}
