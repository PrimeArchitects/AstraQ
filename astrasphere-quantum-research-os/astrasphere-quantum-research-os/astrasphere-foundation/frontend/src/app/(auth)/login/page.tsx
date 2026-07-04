"use client";

import type { Route } from "next";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { signIn } from "next-auth/react";
import { Suspense, useState } from "react";

import { GoogleSignInButton } from "@/components/auth/google-signin-button";
import { Button } from "@/components/ui/button";
import { FormMessage } from "@/components/ui/form-message";
import { Input } from "@/components/ui/input";
import { Panel } from "@/components/ui/panel";

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") ?? "/";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    const result = await signIn("credentials", { email, password, redirect: false });

    setIsSubmitting(false);
    if (result?.error) {
      // Auth.js's Credentials provider returning `null` from authorize()
      // surfaces here as a generic "CredentialsSignin" — the backend
      // already collapses "no such user" and "wrong password" into one
      // message (see docs/authentication.md), so we mirror that here.
      setError("Incorrect email or password.");
      return;
    }
    router.push(callbackUrl as Route);
  }

  return (
    <Panel>
      <h1 className="mb-1 font-display text-display-sm text-foreground">Sign in</h1>
      <p className="mb-6 text-body-sm text-foreground-muted">
        Welcome back to your research console.
      </p>

      {error && <FormMessage variant="error">{error}</FormMessage>}

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
        <div>
          <div className="mb-1.5 flex items-center justify-between">
            <label htmlFor="password" className="block text-body-sm text-foreground-muted">
              Password
            </label>
            <Link
              href="/forgot-password"
              className="text-body-sm text-signal hover:text-signal-bright"
            >
              Forgot password?
            </Link>
          </div>
          <Input
            id="password"
            type="password"
            autoComplete="current-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? "Signing in..." : "Sign in"}
        </Button>
      </form>

      <div className="my-5 flex items-center gap-3">
        <div className="h-px flex-1 bg-line" />
        <span className="font-mono text-label uppercase tracking-widest text-foreground-faint">
          or
        </span>
        <div className="h-px flex-1 bg-line" />
      </div>

      <GoogleSignInButton callbackUrl={callbackUrl} />

      <p className="mt-6 text-center text-body-sm text-foreground-muted">
        Don&rsquo;t have an account?{" "}
        <Link href="/signup" className="text-signal hover:text-signal-bright">
          Sign up
        </Link>
      </p>
    </Panel>
  );
}

export default function LoginPage() {
  return (
    <Suspense>
      <LoginForm />
    </Suspense>
  );
}
