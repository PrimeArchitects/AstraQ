"use client";

import { useState } from "react";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Panel, PanelLabel } from "@/components/ui/panel";
import { SwitchRow } from "@/components/ui/switch";
import { CURRENT_USER } from "@/data/mock";

/**
 * Form state is local-only — nothing persists. `handleSave` is the seam
 * where a real PATCH /users/me mutation attaches once the backend has
 * an endpoint for it.
 */
export default function SettingsPage() {
  const [name, setName] = useState(CURRENT_USER.name);
  const [email, setEmail] = useState(CURRENT_USER.email);
  const [notifications, setNotifications] = useState({
    citations: true,
    comments: true,
    weeklyDigest: false,
  });

  return (
    <AppShell>
      <div className="mx-auto max-w-2xl">
        <PageHeader title="Settings" description="Manage your profile and preferences." />

        <div className="flex flex-col gap-6">
          <Panel>
            <PanelLabel>Profile</PanelLabel>
            <div className="mb-5 flex items-center gap-3">
              <Avatar className="h-12 w-12">
                <AvatarFallback className="text-title">{CURRENT_USER.initials}</AvatarFallback>
              </Avatar>
              <div>
                <p className="text-body-sm text-foreground">{CURRENT_USER.role}</p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <label htmlFor="name" className="mb-1.5 block text-body-sm text-foreground-muted">
                  Full name
                </label>
                <Input id="name" value={name} onChange={(e) => setName(e.target.value)} />
              </div>
              <div>
                <label htmlFor="email" className="mb-1.5 block text-body-sm text-foreground-muted">
                  Email
                </label>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>
            <div className="mt-5 flex justify-end">
              <Button size="sm">Save changes</Button>
            </div>
          </Panel>

          <Panel>
            <PanelLabel>Notifications</PanelLabel>
            <div className="divide-y divide-line-faint">
              <SwitchRow
                id="notif-citations"
                label="New citations"
                description="Get notified when your work is cited."
                checked={notifications.citations}
                onCheckedChange={(v) => setNotifications((s) => ({ ...s, citations: v }))}
              />
              <SwitchRow
                id="notif-comments"
                label="Comments"
                description="Get notified about comments on your papers."
                checked={notifications.comments}
                onCheckedChange={(v) => setNotifications((s) => ({ ...s, comments: v }))}
              />
              <SwitchRow
                id="notif-digest"
                label="Weekly digest"
                description="A summary of trending topics in your field."
                checked={notifications.weeklyDigest}
                onCheckedChange={(v) => setNotifications((s) => ({ ...s, weeklyDigest: v }))}
              />
            </div>
          </Panel>
        </div>
      </div>
    </AppShell>
  );
}
