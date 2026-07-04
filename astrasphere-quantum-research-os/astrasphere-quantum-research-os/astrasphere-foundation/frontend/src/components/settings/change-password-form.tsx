"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { FormMessage } from "@/components/ui/form-message";
import { Input } from "@/components/ui/input";
import { ApiError, apiClient } from "@/lib/api-client";

/** On success, the backend revokes all sessions (see auth_service.py's
 * change_password) — the user is signed out and redirected to log back in. */
export function ChangePasswordForm() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await apiClient.post("/auth/change-password", {
        current_password: currentPassword,
        new_password: newPassword,
      });
      setSuccess(true);
      setTimeout(() => {
        window.location.href = "/login";
      }, 1500);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        setError("Current password is incorrect.");
      } else if (err instanceof ApiError && err.status === 422) {
        setError(err.detail);
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  if (success) {
    return (
      <FormMessage variant="success">
        Password changed. You&rsquo;ve been signed out for security — redirecting to sign in...
      </FormMessage>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      {error && <FormMessage variant="error">{error}</FormMessage>}
      <div>
        <label
          htmlFor="currentPassword"
          className="mb-1.5 block text-body-sm text-foreground-muted"
        >
          Current password
        </label>
        <Input
          id="currentPassword"
          type="password"
          autoComplete="current-password"
          required
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="newPassword" className="mb-1.5 block text-body-sm text-foreground-muted">
          New password
        </label>
        <Input
          id="newPassword"
          type="password"
          autoComplete="new-password"
          required
          minLength={10}
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
      </div>
      <Button type="submit" size="sm" disabled={isSubmitting}>
        {isSubmitting ? "Changing..." : "Change password"}
      </Button>
    </form>
  );
}
