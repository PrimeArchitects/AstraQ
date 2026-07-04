import type { DefaultSession } from "next-auth";

/** Module augmentation: adds the backend user id + verification status
 * to Auth.js's session/user types so they're available without casts. */
declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      emailVerified: Date | null;
    } & DefaultSession["user"];
  }

  interface User {
    emailVerified?: Date | null;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    id?: string;
    emailVerified?: Date | null;
  }
}
