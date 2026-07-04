"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";

import { Button } from "@/components/ui/button";
import { FormMessage } from "@/components/ui/form-message";
import { Input } from "@/components/ui/input";
import { Panel } from "@/components/ui/panel";
import { ApiError, apiClient } from "@/lib/api-client";

function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!token) {
    return (
      <Panel>
        <FormMessage variant="error">
          This reset link is missing its token. Request a new one from the forgot-password page.
        </FormMessage>
        <Link href="/forgot-password" className="text-body-sm text-signal hover:text-signal-bright">
          Request a new link
        </Link>
      </Panel>
    );
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await apiClient.post("/auth/reset-password", { token, new_password: newPassword });
      setSuccess(true);
      setTimeout(() => router.push("/login"), 2000);
    } catch (err) {
      if (err instanceof ApiError && err.status === 422) {
        setError(err.detail || "This reset link is invalid or has expired. Request a new one.");
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Panel>
      <h1 className="mb-1 font-display text-display-sm text-foreground">Set a new password</h1>
      <p className="mb-6 text-body-sm text-foreground-muted">
        Choose a new password for your account.
      </p>

      {error && <FormMessage variant="error">{error}</FormMessage>}
      {success && (
        <FormMessage variant="success">Password reset. Redirecting you to sign in...</FormMessage>
      )}

      {!success && (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="newPassword"
              className="mb-1.5 block text-body-sm text-foreground-muted"
            >
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
          <Button type="submit" className="w-full" disabled={isSubmitting}>
            {isSubmitting ? "Resetting..." : "Reset password"}
          </Button>
        </form>
      )}
    </Panel>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense>
      <ResetPasswordForm />
    </Suspense>
  );
}
