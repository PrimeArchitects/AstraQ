# Authentication & User Management

## Architecture decision: why not Clerk

The brief's first choice was Clerk. Clerk is a fully **hosted** identity
provider — it stores the user record in Clerk's own cloud, not in a
database this project controls. That's a direct conflict with this
phase's explicit requirement to own **Users / Sessions / User
Preferences / Auth Providers** as tables in our own Postgres, managed
through Alembic migrations. There's also no way to provision a real
Clerk account or live Google OAuth credentials inside the environment
this was built in, so a Clerk integration couldn't be verified
end-to-end — only self-hosted auth could be.

So: **Auth.js (NextAuth v5)**, the specified fallback — but configured
in the one way that's actually consistent with the rest of this
project's architecture:

```
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│   Browser    │────────▶│   Next.js     │────────▶│   FastAPI     │
│              │◀────────│  (Auth.js)    │◀────────│   (backend)   │
└─────────────┘         └──────────────┘         └──────────────┘
  Sends both cookie      Session strategy:         Owns Users,
  jars automatically      JWT only, no DB           Sessions,
  (same registrable       adapter. Credentials      AuthProviders,
  site in dev; shared     provider calls the        UserPreferences.
  parent domain in        backend and forwards      Issues its own
  production)             its Set-Cookie            httpOnly access/
                          headers to the browser.    refresh/CSRF
                                                      cookies. Bcrypt
                                                      password hashing,
                                                      JWT sessions,
                                                      rate limiting,
                                                      all here.
```

**Auth.js owns only the frontend session cookie.** It has no database
adapter — nothing about it persists to Postgres. The backend is the
single source of truth for identity: it hashes passwords, issues its
own JWTs, tracks sessions, and enforces rate limits. Auth.js's
Credentials provider is a thin bridge: its `authorize()` calls
`POST /auth/login` on the backend and forwards whatever cookies the
backend set onto the browser response, then mints its own short JWT
session (carrying just the user id/email) so Server Components can
read "who's signed in" via `auth()` without an extra network round
trip. Google sign-in uses Auth.js's built-in Google provider the same
way — on success, the backend links or creates the account via
`get_or_create_oauth_user` and issues its own session cookies exactly
as it would for a password login.

This is a standard **BFF (Backend-for-Frontend) pattern**: two
cookie jars, one identity system. If a mobile app is added later, it
skips Auth.js entirely and talks to the same FastAPI endpoints using
`Authorization: Bearer <token>` instead of cookies — see
"Bearer vs. cookie auth" below.

## Data model

```
users                    sessions                 user_preferences         auth_providers
├─ id (uuid, pk)         ├─ id (uuid, pk)          ├─ id (uuid, pk)         ├─ id (uuid, pk)
├─ email (unique, idx)   ├─ user_id (fk→users) idx ├─ user_id (fk, unique)  ├─ user_id (fk) idx
├─ hashed_password?      ├─ refresh_token_hash     ├─ theme                ├─ provider
├─ display_name          │    (unique, idx)        ├─ notify_citations     ├─ provider_account_id?
├─ avatar_url?           ├─ user_agent?             ├─ notify_comments      │  (unique w/ provider)
├─ bio?                  ├─ ip_address?             ├─ notify_weekly_digest└─ created_at
├─ institution?          ├─ expires_at              └─ created_at/updated_at
├─ research_interests[]  ├─ revoked_at?
├─ timezone              └─ created_at/updated_at
├─ email_verified
├─ is_active
└─ created_at/updated_at
```

- **`hashed_password` is nullable** — an OAuth-only user (signed up via
  Google, never set a password) has nothing to hash. Password login
  checks this is non-null before attempting verification; account
  deletion skips the password-confirmation step for these accounts.
- **`sessions` stores a hash of the refresh token, never the raw
  value** — the same discipline as password storage. A refresh token
  is rotated (old row revoked, new row issued) on every use, so a
  captured-and-reused token breaks the legitimate session on its next
  refresh — a detectable signal of compromise even without active
  alerting.
- **`auth_providers`** is what "connected login providers" in Settings
  reads from. A user gets a `password` row at registration and/or a
  `google` row after linking Google — both can coexist on one account
  (Google login on an existing email-registered account links rather
  than creating a duplicate user).
- Migration: `backend/alembic/versions/ab0f7f1414de_*.py`, generated
  with `alembic revision --autogenerate` against a real Postgres
  instance and verified with `alembic check` (no drift from the models).

## Request flow

```
Register                          Login                              Refresh
──────────                        ─────                              ───────
POST /auth/register               POST /auth/login                   POST /auth/refresh
 │                                 │                                  │ (refresh cookie)
 ├─ 409 if email taken             ├─ generic 401 whether email        ├─ rotate: revoke old
 ├─ hash password (bcrypt, 12)     │  doesn't exist OR password is     │  session row, issue
 ├─ create user + preferences      │  wrong (no enumeration; a          │  new access+refresh
 │  + "password" provider row      │  dummy-hash comparison keeps       │  cookies
 ├─ issue access/refresh/CSRF      │  response timing constant)        └─ 401 if reused/expired
 │  cookies (same as login)        ├─ issue access/refresh/CSRF
 └─ send verification email        │  cookies
    (logged to console in dev —    └─ 429 after 5 attempts/min/IP
    see app/core/email.py)            (Redis fixed-window)
```

Password reset and email verification both use short-lived, single-
purpose JWTs (`app/core/security.py::TokenPurpose`) — a token minted
for email verification can never be replayed as a password-reset token
or an access token, because the purpose is checked on decode. The
password-reset token additionally embeds a fingerprint of the
password hash at issue time, so it's automatically invalidated the
moment the password actually changes (including by the token's own
use) — no separate token-blocklist table needed.

## Security measures implemented

| Concern | Mechanism |
| --- | --- |
| Password storage | bcrypt via passlib, cost factor 12 |
| Session tokens | Purpose-scoped JWTs (`access`/`refresh`/`email_verification`/`password_reset`) — a token can't be replayed outside its intended use |
| Cookie security | httpOnly, `SameSite=Lax`, `Secure` in staging/prod (`COOKIE_SECURE`) |
| CSRF | Double-submit cookie pattern (`app/core/csrf.py`) on every cookie-authenticated mutating route; Bearer-token requests are exempt (no ambient cookie authority to forge) |
| Rate limiting | Redis fixed-window, per-IP, on register/login/password-reset/resend-verification (`app/core/rate_limit.py`) |
| Enumeration resistance | Login, forgot-password, and resend-verification all return identical responses regardless of whether the account exists |
| Timing side-channels | Login runs a real bcrypt comparison against a dummy hash even when the email doesn't exist, so response time doesn't leak account existence |
| Refresh token rotation | Every refresh revokes the old token and issues a new one; reuse of a revoked token is rejected |
| Session invalidation | Password change and password reset revoke *all* sessions for that user |
| Input validation | Pydantic schemas enforce email format and password strength (≥10 chars, upper+lower+digit) at the API boundary |
| Route protection | `CurrentUser` FastAPI dependency (backend) + Next.js middleware (frontend) both gate on a valid session before any protected data is touched |

## Bearer vs. cookie auth

The backend accepts **either**:
- An httpOnly `astrasphere_access` cookie (how the browser/Next.js
  frontend authenticates), or
- An `Authorization: Bearer <token>` header (for API clients, mobile
  apps, or scripts — anything that isn't a browser with ambient cookie
  ability).

CSRF checks only apply to the cookie path — a Bearer-token request has
no ambient authority for a forged page to hijack, so requiring a CSRF
header for it would be protecting against an attack that doesn't apply.

## Environment variables

**Backend** (`backend/.env`, see `backend/.env.example`):

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Signs all JWTs. Generate a real random value in every non-local environment. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` / `REFRESH_TOKEN_EXPIRE_DAYS` | Session lifetimes |
| `EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS` / `PASSWORD_RESET_TOKEN_EXPIRE_MINUTES` | Link expiry |
| `COOKIE_SECURE` | Set `true` behind HTTPS (staging/production) |
| `COOKIE_DOMAIN` | Set to `.yourdomain.com` in production so the API and frontend subdomains share cookies |
| `RATE_LIMIT_LOGIN_PER_MINUTE` etc. | Per-IP rate limits |
| `FRONTEND_URL` | Used to build links in verification/reset emails |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | Unset by default — Google sign-in is inert until both are provided |

**Frontend** (`frontend/.env.local`, see `frontend/.env.example`):

| Variable | Purpose |
| --- | --- |
| `NEXT_PUBLIC_API_BASE_URL` | Browser-facing backend URL |
| `BACKEND_INTERNAL_URL` | Server-side backend URL (Auth.js's credentials provider runs on the Next.js server) — same value locally, differs in Docker Compose |
| `AUTH_SECRET` | Signs the Auth.js session JWT. Generate with `npx auth secret`. |
| `AUTH_URL` | The frontend's own URL |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | Must match the backend's values exactly |

## OAuth configuration (Google)

Inactive in this environment — no live Google Cloud project exists
here to test against. To enable it in a real environment:

1. In the [Google Cloud Console](https://console.cloud.google.com/),
   create a project (or use an existing one) and open **APIs & Services
   → Credentials**.
2. Create an **OAuth 2.0 Client ID** of type "Web application".
3. Add an authorized redirect URI matching your backend:
   `http://localhost:8000/api/v1/auth/oauth/google/callback` (local) or
   `https://api.yourdomain.com/api/v1/auth/oauth/google/callback`
   (production).
4. Copy the generated Client ID and Client Secret into **both**
   `backend/.env` and `frontend/.env.local` as `GOOGLE_CLIENT_ID` /
   `GOOGLE_CLIENT_SECRET` — they must match, since the frontend's
   Google button and the backend's callback both need to agree on
   which OAuth client this is.
5. Restart both services. The "Continue with Google" button becomes
   live immediately — no code changes needed.

## Local development setup

```bash
# Backend
cd backend
cp .env.example .env               # adjust SECRET_KEY etc.
alembic upgrade head               # creates users/sessions/preferences/auth_providers
uvicorn app.main:app --reload

# Frontend
cd frontend
cp .env.example .env.local
npx auth secret                    # writes AUTH_SECRET into .env.local
npm run dev
```

Both need Postgres and Redis reachable (`docker compose up postgres
redis` from the repo root, or point `POSTGRES_HOST`/`REDIS_HOST` at
existing instances).

## Testing

`backend/tests/` runs against a **real** Postgres and Redis (not
mocks) — password hashing, unique constraints, cascades, and
transaction boundaries are exactly the things worth catching with a
real database:

- `test_security.py` — password hashing and JWT purpose-scoping (unit, no I/O)
- `test_validation.py` — schema-level password strength / email format rules (unit, no I/O)
- `test_auth.py` — registration, login, session refresh/rotation, logout, email verification, password reset (integration)
- `test_user.py` — profile updates, preferences, connected providers, change password, account deletion (integration)
- `test_route_protection.py` — anonymous rejection, tampered/expired tokens, Bearer-vs-cookie auth, CSRF exemption for Bearer clients (integration)

```bash
cd backend
POSTGRES_DB=astrasphere_test alembic upgrade head   # once, against a dedicated test DB
POSTGRES_DB=astrasphere_test pytest -v
```

63 tests, all passing against real infrastructure — see `make test-backend`.

Frontend verification for this phase is `npm run typecheck`, `npm run
lint`, and `npm run build` (all clean, all 21 routes including the new
auth pages) — a full browser-driven end-to-end test of the login/OAuth
flow requires a running browser and isn't something this environment
can execute.
