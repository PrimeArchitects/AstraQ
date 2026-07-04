/** Shared frontend types. Feature-specific types live alongside their feature. */

export interface ApiError {
  error: string;
  detail: string;
}

export type SystemStatus = "nominal" | "degraded" | "offline";

/** Mirrors backend app/schemas/user.py — keep in sync manually until
 * shared/openapi/ generates this. */
export interface UserProfile {
  id: string;
  email: string;
  display_name: string;
  avatar_url: string | null;
  bio: string | null;
  institution: string | null;
  research_interests: string[];
  timezone: string;
  email_verified: boolean;
  created_at: string;
}

export interface UserPreferences {
  theme: "light" | "dark";
  notify_citations: boolean;
  notify_comments: boolean;
  notify_weekly_digest: boolean;
}

export interface AuthProviderLink {
  provider: string;
  created_at: string;
}
