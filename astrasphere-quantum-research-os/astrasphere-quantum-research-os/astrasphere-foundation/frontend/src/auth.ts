import NextAuth, { type NextAuthConfig } from "next-auth";
import Credentials from "next-auth/providers/credentials";
import Google from "next-auth/providers/google";
import { cookies } from "next/headers";

import { getBackendUrl } from "@/lib/backend-url";

/**
 * Auth.js (NextAuth v5) session/identity layer for the frontend.
 *
 * Architecture: Auth.js owns ONLY the frontend session cookie (JWT
 * strategy, no database adapter). The FastAPI backend remains the
 * source of truth for users, password hashing, and sessions — it owns
 * its own httpOnly cookies (access/refresh/CSRF tokens), set directly
 * on the browser via `credentials.authorize()` below forwarding the
 * backend's Set-Cookie headers. Auth.js's session JWT just carries the
 * backend user id/email/display name so server components can read
 * "who is logged in" without an extra round trip.
 *
 * This split exists because Clerk (the first-choice tool) is a fully
 * hosted identity provider that would own the user table itself —
 * incompatible with this project's requirement that Users/Sessions/
 * AuthProviders live in our own Postgres via Alembic migrations. See
 * docs/authentication.md for the full rationale.
 */

const credentialsProvider = Credentials({
  id: "credentials",
  name: "Email and password",
  credentials: {
    email: { label: "Email", type: "email" },
    password: { label: "Password", type: "password" },
  },
  async authorize(rawCredentials) {
    const email = rawCredentials?.email;
    const password = rawCredentials?.password;
    if (typeof email !== "string" || typeof password !== "string") {
      return null;
    }

    const response = await fetch(`${getBackendUrl()}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      return null;
    }

    // Forward the backend's session cookies (access/refresh/CSRF) onto
    // the browser response. The backend, not Auth.js, is what actually
    // authenticates subsequent API calls — this just makes sure the
    // cookies it issued during this login actually reach the client.
    const cookieStore = await cookies();
    for (const setCookieHeader of response.headers.getSetCookie()) {
      const pair = setCookieHeader.split(";")[0];
      if (!pair) continue;
      const eqIndex = pair.indexOf("=");
      const name = pair.slice(0, eqIndex);
      const value = pair.slice(eqIndex + 1);
      const attrs = setCookieHeader.toLowerCase();
      cookieStore.set(name, value, {
        httpOnly: attrs.includes("httponly"),
        secure: attrs.includes("secure"),
        sameSite: "lax",
        path: "/",
      });
    }

    const user = await response.json();
    return {
      id: user.id,
      email: user.email,
      name: user.display_name,
      emailVerified: user.email_verified ? new Date() : null,
    };
  },
});

const providers: NextAuthConfig["providers"] = [credentialsProvider];

// Google sign-in is only registered when real credentials are
// configured — see docs/authentication.md "OAuth configuration". This
// environment has no live Google Cloud project, so it's absent here
// but wires up automatically once GOOGLE_CLIENT_ID/SECRET are set.
if (process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET) {
  providers.push(
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
  );
}

export const authConfig: NextAuthConfig = {
  providers,
  session: { strategy: "jwt" },
  pages: {
    signIn: "/login",
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.emailVerified = user.emailVerified ?? null;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.emailVerified = (token.emailVerified as Date | null) ?? null;
      }
      return session;
    },
  },
};

export const { handlers, auth, signIn, signOut } = NextAuth(authConfig);
