import { NextResponse } from "next/server";

import { auth } from "@/auth";

/**
 * Route protection: anonymous visitors hitting anything not on the
 * public allow-list are redirected to /login (with a `callbackUrl` so
 * they land back where they meant to go after signing in).
 *
 * "Role-ready": `session.user` doesn't carry a role today (the backend
 * has no roles concept yet), but the check below is structured as a
 * single gate function so adding `if (!hasRole(session, "admin"))`
 * per-route later is a small addition here, not a rewrite.
 */
const PUBLIC_ROUTES = ["/login", "/signup", "/forgot-password", "/reset-password", "/verify-email"];

function isPublicRoute(pathname: string): boolean {
  return PUBLIC_ROUTES.some((route) => pathname === route || pathname.startsWith(`${route}/`));
}

export default auth((req) => {
  const { pathname } = req.nextUrl;

  if (isPublicRoute(pathname)) {
    // Signed-in users don't need to see auth forms again.
    if (req.auth && (pathname === "/login" || pathname === "/signup")) {
      return NextResponse.redirect(new URL("/", req.nextUrl));
    }
    return NextResponse.next();
  }

  if (!req.auth) {
    const loginUrl = new URL("/login", req.nextUrl);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
});

export const config = {
  // Exclude static assets, images, and Next.js internals — those are
  // always "public" and matching them would be wasted middleware work.
  matcher: ["/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|webp)$).*)"],
};
