import type { NextConfig } from "next";

/**
 * Central Next.js configuration.
 *
 * `reactStrictMode` and typed routes are on by default for a foundation
 * repo — catch class-of-bug issues early rather than after feature teams
 * have built on top. Remote image domains / rewrites for the backend API
 * gateway get added here as those integrations land.
 */
const nextConfig: NextConfig = {
  reactStrictMode: true,
  typedRoutes: true,
  output: "standalone",
  eslint: {
    dirs: ["src"],
  },
};

export default nextConfig;
