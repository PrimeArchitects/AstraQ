"use client";

import { MailCheck } from "lucide-react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { FormMessage } from "@/components/ui/form-message";
import { Input } from "@/components/ui/input";
import { Panel } from "@/components/ui/panel";
import { ApiError, apiClient } from "@/lib/api-client";

type VerificationState = "pending" | "verifying" | "success" | "error" | "awaiting-link";

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const justRegistered = searchParams.get("justRegistered") === "true";

  const [state, setState] = useState<VerificationState>(
    token ? "verifying" : justRegistered ? "awaiting-link" : "pending",
  );
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [resendEmail, setResendEmail] = useState("");
  const [resendSent, setResendSent] = useState(false);

  useEffect(() => {
    if (!token) return;
    apiClient
      .get(`/auth/verify-email?token=${encodeURIComponent(token)}`)
      .then(() => setState("success"))
      .catch((err: unknown) => {
        setState("error");
        setErrorMessage(
          err instanceof ApiError
            ? err.detail
            : "This verification link is invalid or has expired.",
        );
      });
  }, [token]);

  async function handleResend(e: React.FormEvent) {
    e.preventDefault();
    await apiClient.post("/auth/verify-email/resend", { email: resendEmail });
    setResendSent(true);
  }

  if (state === "verifying") {
    return (
      <Panel className="text-center">
        <p className="text-body-sm text-foreground-muted">Verifying your email...</p>
      </Panel>
    );
  }

  if (state === "success") {
    return (
      <Panel className="text-center">
        <MailCheck className="mx-auto mb-3 h-8 w-8 text-signal" aria-hidden />
        <h1 className="mb-2 font-display text-display-sm text-foreground">Email verified</h1>
        <p className="mb-6 text-body-sm text-foreground-muted">Your account is fully set up.</p>
        <Link href="/">
          <Button className="w-full">Go to your console</Button>
        </Link>
      </Panel>
    );
  }

  if (state === "error") {
    return (
      <Panel>
        <FormMessage variant="error">
          {errorMessage ?? "This verification link is invalid or has expired."}
        </FormMessage>
        <form onSubmit={handleResend} className="space-y-3">
          <Input
            type="email"
            placeholder="you@example.com"
            required
            value={resendEmail}
            onChange={(e) => setResendEmail(e.target.value)}
          />
          <Button type="submit" className="w-full" disabled={resendSent}>
            {resendSent ? "New link sent" : "Send a new link"}
          </Button>
        </form>
      </Panel>
    );
  }

  // "pending" or "awaiting-link" — no token in the URL yet.
  return (
    <Panel className="text-center">
      <MailCheck className="mx-auto mb-3 h-8 w-8 text-entangled" aria-hidden />
      <h1 className="mb-2 font-display text-display-sm text-foreground">Check your email</h1>
      <p className="mb-6 text-body-sm text-foreground-muted">
        We sent a verification link to your inbox. Click it to activate your account.
      </p>
      {resendSent ? (
        <FormMessage variant="success">New link sent — check your inbox.</FormMessage>
      ) : (
        <form onSubmit={handleResend} className="space-y-3 text-left">
          <label htmlFor="resendEmail" className="block text-body-sm text-foreground-muted">
            Didn&rsquo;t get it? Resend to:
          </label>
          <Input
            id="resendEmail"
            type="email"
            required
            value={resendEmail}
            onChange={(e) => setResendEmail(e.target.value)}
          />
          <Button type="submit" variant="outline" className="w-full">
            Resend link
          </Button>
        </form>
      )}
    </Panel>
  );
}

export default function VerifyEmailPage() {
  return (
    <Suspense>
      <VerifyEmailContent />
    </Suspense>
  );
}
