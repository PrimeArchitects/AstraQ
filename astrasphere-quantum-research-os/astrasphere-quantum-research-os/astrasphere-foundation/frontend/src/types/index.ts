/** Shared frontend types. Feature-specific types live alongside their feature. */

export interface ApiError {
  error: string;
  detail: string;
}

export type SystemStatus = "nominal" | "degraded" | "offline";
