"use client";

import Link from "next/link";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { FormMessage } from "@/components/ui/form-message";
import { Input } from "@/components/ui/input";
import { Panel } from "@/components/ui/panel";
import { apiClient } from "@/lib/api-client";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await apiClient.post("/auth/forgot-password", { email });
    } finally {
      // Always show the same confirmation regardless of outcome — the
      // backend deliberately returns an identical response whether or
      // not the email is registered, to avoid leaking account existence.
      setIsSubmitting(false);
      setSubmitted(true);
    }
  }

  return (
    <Panel>
      <h1 className="mb-1 font-display text-display-sm text-foreground">Reset your password</h1>
      <p className="mb-6 text-body-sm text-foreground-muted">
        Enter your email and we&rsquo;ll send you a reset link.
      </p>

      {submitted ? (
        <FormMessage variant="success">
          If that email is registered, a reset link is on its way. Check your inbox.
        </FormMessage>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="mb-1.5 block text-body-sm text-foreground-muted">
              Email
            </label>
            <Input
              id="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <Button type="submit" className="w-full" disabled={isSubmitting}>
            {isSubmitting ? "Sending..." : "Send reset link"}
          </Button>
        </form>
      )}

      <p className="mt-6 text-center text-body-sm text-foreground-muted">
        <Link href="/login" className="text-signal hover:text-signal-bright">
          Back to sign in
        </Link>
      </p>
    </Panel>
  );
}
