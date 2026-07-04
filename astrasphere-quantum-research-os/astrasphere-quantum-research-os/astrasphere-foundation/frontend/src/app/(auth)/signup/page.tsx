"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { signIn } from "next-auth/react";
import { useState } from "react";

import { GoogleSignInButton } from "@/components/auth/google-signin-button";
import { Button } from "@/components/ui/button";
import { FormMessage } from "@/components/ui/form-message";
import { Input } from "@/components/ui/input";
import { Panel } from "@/components/ui/panel";
import { ApiError, apiClient } from "@/lib/api-client";

const PASSWORD_REQUIREMENTS =
  "At least 10 characters, with an uppercase letter, a lowercase letter, and a number.";

export default function SignupPage() {
  const router = useRouter();

  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      // The backend is the source of truth for the account itself.
      await apiClient.post("/auth/register", {
        email,
        password,
        display_name: displayName,
      });
    } catch (err) {
      setIsSubmitting(false);
      if (err instanceof ApiError) {
        if (err.status === 409) {
          setError("An account with this email already exists. Try signing in instead.");
        } else if (err.status === 422) {
          setError(err.detail || PASSWORD_REQUIREMENTS);
        } else {
          setError("Something went wrong. Please try again.");
        }
      } else {
        setError("Network error. Check your connection and try again.");
      }
      return;
    }

    // Establish the Auth.js session too, so the frontend's notion of
    // "signed in" matches the account the backend just created.
    await signIn("credentials", { email, password, redirect: false });
    setIsSubmitting(false);
    router.push("/verify-email?justRegistered=true");
  }

  return (
    <Panel>
      <h1 className="mb-1 font-display text-display-sm text-foreground">Create your account</h1>
      <p className="mb-6 text-body-sm text-foreground-muted">
        Start organizing your quantum research today.
      </p>

      {error && <FormMessage variant="error">{error}</FormMessage>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="displayName" className="mb-1.5 block text-body-sm text-foreground-muted">
            Full name
          </label>
          <Input
            id="displayName"
            autoComplete="name"
            required
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
          />
        </div>
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
          <label htmlFor="password" className="mb-1.5 block text-body-sm text-foreground-muted">
            Password
          </label>
          <Input
            id="password"
            type="password"
            autoComplete="new-password"
            required
            minLength={10}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <p className="mt-1.5 text-body-sm text-foreground-faint">{PASSWORD_REQUIREMENTS}</p>
        </div>
        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? "Creating account..." : "Create account"}
        </Button>
      </form>

      <div className="my-5 flex items-center gap-3">
        <div className="h-px flex-1 bg-line" />
        <span className="font-mono text-label uppercase tracking-widest text-foreground-faint">
          or
        </span>
        <div className="h-px flex-1 bg-line" />
      </div>

      <GoogleSignInButton />

      <p className="mt-6 text-center text-body-sm text-foreground-muted">
        Already have an account?{" "}
        <Link href="/login" className="text-signal hover:text-signal-bright">
          Sign in
        </Link>
      </p>
    </Panel>
  );
}
