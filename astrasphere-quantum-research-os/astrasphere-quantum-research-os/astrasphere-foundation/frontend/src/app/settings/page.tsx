"use client";

import { useEffect, useState } from "react";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { ChangePasswordForm } from "@/components/settings/change-password-form";
import { ConnectedProviders } from "@/components/settings/connected-providers";
import { DeleteAccountModal } from "@/components/settings/delete-account-modal";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { ErrorState } from "@/components/ui/error-state";
import { Input } from "@/components/ui/input";
import { Panel, PanelLabel } from "@/components/ui/panel";
import { Skeleton } from "@/components/ui/skeleton";
import { SwitchRow } from "@/components/ui/switch";
import {
  useAuthProviders,
  usePreferences,
  useProfile,
  useUpdatePreferences,
  useUpdateProfile,
} from "@/hooks/use-profile";

function initials(name: string): string {
  return name
    .split(" ")
    .map((p) => p[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

function ProfileSection() {
  const { data: profile, isLoading, isError, refetch } = useProfile();
  const updateProfile = useUpdateProfile();

  const [displayName, setDisplayName] = useState("");
  const [institution, setInstitution] = useState("");
  const [bio, setBio] = useState("");
  const [interests, setInterests] = useState("");

  useEffect(() => {
    if (!profile) return;
    setDisplayName(profile.display_name);
    setInstitution(profile.institution ?? "");
    setBio(profile.bio ?? "");
    setInterests(profile.research_interests.join(", "));
  }, [profile]);

  if (isLoading) return <Skeleton className="h-64" />;
  if (isError) return <ErrorState onRetry={() => refetch()} />;
  if (!profile) return null;

  function handleSave() {
    updateProfile.mutate({
      display_name: displayName,
      institution: institution || null,
      bio: bio || null,
      research_interests: interests
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean),
    });
  }

  return (
    <Panel>
      <PanelLabel>Profile</PanelLabel>
      <div className="mb-5 flex items-center gap-3">
        <Avatar className="h-12 w-12">
          <AvatarFallback className="text-title">{initials(profile.display_name)}</AvatarFallback>
        </Avatar>
        <p className="text-body-sm text-foreground-faint">{profile.email}</p>
      </div>
      <div className="space-y-4">
        <div>
          <label htmlFor="displayName" className="mb-1.5 block text-body-sm text-foreground-muted">
            Full name
          </label>
          <Input
            id="displayName"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="institution" className="mb-1.5 block text-body-sm text-foreground-muted">
            Institution
          </label>
          <Input
            id="institution"
            value={institution}
            onChange={(e) => setInstitution(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="bio" className="mb-1.5 block text-body-sm text-foreground-muted">
            Bio
          </label>
          <textarea
            id="bio"
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            rows={3}
            className="w-full rounded-control border border-line bg-ink-raised px-3 py-2 text-body text-foreground placeholder:text-foreground-faint focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-signal"
          />
        </div>
        <div>
          <label htmlFor="interests" className="mb-1.5 block text-body-sm text-foreground-muted">
            Research interests (comma-separated)
          </label>
          <Input
            id="interests"
            value={interests}
            onChange={(e) => setInterests(e.target.value)}
            placeholder="error correction, photonics"
          />
        </div>
      </div>
      <div className="mt-5 flex items-center justify-end gap-3">
        {updateProfile.isSuccess && <span className="text-body-sm text-signal">Saved</span>}
        <Button size="sm" onClick={handleSave} disabled={updateProfile.isPending}>
          {updateProfile.isPending ? "Saving..." : "Save changes"}
        </Button>
      </div>
    </Panel>
  );
}

function PreferencesSection() {
  const { data: prefs, isLoading } = usePreferences();
  const updatePreferences = useUpdatePreferences();

  if (isLoading || !prefs) return <Skeleton className="h-48" />;

  return (
    <Panel>
      <PanelLabel>Preferences</PanelLabel>
      <div className="mb-2">
        <p className="mb-1.5 text-body-sm text-foreground-muted">Theme</p>
        <div className="flex gap-2">
          {(["dark", "light"] as const).map((theme) => (
            <Button
              key={theme}
              size="sm"
              variant={prefs.theme === theme ? "default" : "outline"}
              onClick={() => updatePreferences.mutate({ theme })}
              className="capitalize"
            >
              {theme}
            </Button>
          ))}
        </div>
      </div>
      <div className="mt-4 divide-y divide-line-faint border-t border-line-faint">
        <SwitchRow
          id="notify_citations"
          label="New citations"
          description="Get notified when your work is cited."
          checked={prefs.notify_citations}
          onCheckedChange={(v) => updatePreferences.mutate({ notify_citations: v })}
        />
        <SwitchRow
          id="notify_comments"
          label="Comments"
          description="Get notified about comments on your papers."
          checked={prefs.notify_comments}
          onCheckedChange={(v) => updatePreferences.mutate({ notify_comments: v })}
        />
        <SwitchRow
          id="notify_weekly_digest"
          label="Weekly digest"
          description="A summary of trending topics in your field. (Sending not yet implemented — see app/core/email.py.)"
          checked={prefs.notify_weekly_digest}
          onCheckedChange={(v) => updatePreferences.mutate({ notify_weekly_digest: v })}
        />
      </div>
    </Panel>
  );
}

function DangerZoneSection() {
  const { data: providers } = useAuthProviders();
  const hasPassword = providers?.some((p) => p.provider === "password") ?? true;

  return (
    <Panel className="border-critical/30">
      <PanelLabel>Danger Zone</PanelLabel>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-body-sm text-foreground">Delete account</p>
          <p className="text-body-sm text-foreground-faint">
            Permanently delete your account and all associated data.
          </p>
        </div>
        <DeleteAccountModal
          hasPassword={hasPassword}
          trigger={
            <Button variant="destructive" size="sm">
              Delete account
            </Button>
          }
        />
      </div>
    </Panel>
  );
}

export default function SettingsPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-2xl">
        <PageHeader title="Settings" description="Manage your profile and preferences." />
        <div className="flex flex-col gap-6">
          <ProfileSection />

          <Panel>
            <PanelLabel>Security</PanelLabel>
            <ChangePasswordForm />
          </Panel>

          <Panel>
            <PanelLabel>Connected Login Providers</PanelLabel>
            <ConnectedProviders />
          </Panel>

          <PreferencesSection />

          <DangerZoneSection />
        </div>
      </div>
    </AppShell>
  );
}
