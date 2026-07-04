"use client";

import { Building2, Calendar, Globe, Pencil } from "lucide-react";
import Link from "next/link";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ErrorState } from "@/components/ui/error-state";
import { Panel, PanelLabel } from "@/components/ui/panel";
import { Skeleton } from "@/components/ui/skeleton";
import { useProfile } from "@/hooks/use-profile";

function initials(name: string): string {
  return name
    .split(" ")
    .map((part) => part[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

export default function ProfilePage() {
  const { data: profile, isLoading, isError, refetch } = useProfile();

  return (
    <AppShell>
      <div className="mx-auto max-w-3xl">
        <PageHeader
          title="Profile"
          description="How other researchers see you across AstraSphere."
          action={
            <Link href="/settings">
              <Button size="sm" variant="outline" className="gap-1.5">
                <Pencil className="h-3.5 w-3.5" aria-hidden />
                Edit in Settings
              </Button>
            </Link>
          }
        />

        {isLoading && <Skeleton className="h-64" />}
        {isError && <ErrorState onRetry={() => refetch()} />}

        {profile && (
          <div className="flex flex-col gap-4">
            <Panel>
              <div className="flex items-start gap-4">
                <Avatar className="h-16 w-16">
                  <AvatarFallback className="text-title">
                    {initials(profile.display_name)}
                  </AvatarFallback>
                </Avatar>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <h2 className="font-display text-title text-foreground">
                      {profile.display_name}
                    </h2>
                    {!profile.email_verified && <Badge variant="warning">Unverified</Badge>}
                  </div>
                  <p className="text-body-sm text-foreground-faint">{profile.email}</p>
                  {profile.bio && (
                    <p className="mt-3 text-body-sm text-foreground-muted">{profile.bio}</p>
                  )}
                </div>
              </div>

              <dl className="mt-5 grid grid-cols-1 gap-3 border-t border-line-faint pt-4 sm:grid-cols-2">
                {profile.institution && (
                  <div className="flex items-center gap-2">
                    <Building2 className="h-4 w-4 shrink-0 text-foreground-faint" aria-hidden />
                    <dd className="text-body-sm text-foreground">{profile.institution}</dd>
                  </div>
                )}
                <div className="flex items-center gap-2">
                  <Globe className="h-4 w-4 shrink-0 text-foreground-faint" aria-hidden />
                  <dd className="text-body-sm text-foreground">{profile.timezone}</dd>
                </div>
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 shrink-0 text-foreground-faint" aria-hidden />
                  <dd className="text-body-sm text-foreground">
                    Joined {new Date(profile.created_at).toLocaleDateString()}
                  </dd>
                </div>
              </dl>
            </Panel>

            <Panel>
              <PanelLabel>Research Interests</PanelLabel>
              {profile.research_interests.length === 0 ? (
                <p className="text-body-sm text-foreground-faint">
                  No research interests added yet.
                </p>
              ) : (
                <div className="flex flex-wrap gap-2">
                  {profile.research_interests.map((interest) => (
                    <Badge key={interest} variant="info">
                      {interest}
                    </Badge>
                  ))}
                </div>
              )}
            </Panel>
          </div>
        )}
      </div>
    </AppShell>
  );
}
