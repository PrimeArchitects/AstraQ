# Design System

The console UI is an **instrument-panel aesthetic** — near-black
surfaces, a phosphor-cyan accent, monospace data readouts, and
corner-bracketed panels — rather than a generic SaaS dashboard. Dark
mode is the primary experience; light mode is fully supported via CSS
variables for accessibility and daytime use.

All tokens live in `frontend/tailwind.config.ts` and
`frontend/src/app/globals.css`. Components should reference tokens
(`bg-ink-panel`, `text-foreground-muted`, `text-title`) — never
hardcode a hex value or arbitrary pixel size.

## Color palette

| Token | Role |
| --- | --- |
| `ink` / `ink-panel` / `ink-raised` | Background layers, darkest to lightest (theme-aware) |
| `line` / `line-faint` / `line-strong` | Borders and dividers (theme-aware) |
| `foreground` / `foreground-muted` / `foreground-faint` | Text, in descending emphasis (theme-aware) |
| `signal` | Brand accent — primary actions, active nav, positive trend |
| `pulse` | Secondary accent — warnings, priority markers |
| `entangled` | Tertiary accent — AI/insight content, data viz |
| `danger` | Destructive actions, errors |
| `success` / `warning` / `info` / `critical` | Semantic aliases for badges/status — use these over brand names when the intent is status, not chrome |

`ink`, `line`, and `foreground` are defined as CSS variables
(`--color-ink`, etc.) in `globals.css`, redefined under `.dark` — this
is what makes the theme toggle produce a real, correctly-contrasted
light mode rather than a cosmetic flip.

## Typography scale

Defined in `tailwind.config.ts` under `fontSize`. Use these classes,
not raw Tailwind sizes:

| Class | Use |
| --- | --- |
| `text-display-lg` / `-md` / `-sm` | Page and section headings |
| `text-title` | Card/panel titles |
| `text-body` | Default body copy |
| `text-body-sm` | Secondary copy, table cells, descriptions |
| `text-label` | Uppercase mono labels (nav groups, panel labels) |
| `text-data` / `text-data-lg` | Monospace numeric readouts |

Three font families, loaded via `next/font/google` in
`app/layout.tsx`: **Space Grotesk** (`font-display`, headings),
**Inter** (`font-body`, default), **IBM Plex Mono** (`font-mono`, data
and labels).

## Spacing

Tailwind's default spacing scale (4px base unit) is used as-is — no
custom overrides. Card/panel padding is `p-5` or `p-6`; section gaps
are `gap-4`–`gap-8`. Consistency comes from reusing `DashboardCard` and
`Panel` rather than from a bespoke spacing token set.

## Elevation & layering

| Token | Use |
| --- | --- |
| `shadow-panel` | Subtle inset highlight on panels |
| `shadow-raised` | Modals, dropdowns — anything floating above content |
| `shadow-glow` | Signal-colored focus glow (used sparingly) |
| `z-chrome` / `z-overlay` / `z-modal` / `z-toast` | Stacking contract — reference these instead of ad hoc z-index values |

## Component library

All in `frontend/src/components/ui/`:

| Component | Notes |
| --- | --- |
| `Button` | `default` / `outline` / `ghost` / `destructive` variants, `sm`/`default`/`lg` sizes (cva-based) |
| `Panel` | Signature corner-bracketed container — the base for every data surface |
| `Badge` | Status pill — `neutral`/`success`/`warning`/`info`/`critical` |
| `Progress` | Linear progress bar, `role="progressbar"` with proper aria attributes |
| `Skeleton` | Shimmer loading placeholder |
| `EmptyState` | "Nothing here" treatment — used by every unbuilt route and empty list |
| `ErrorState` | Failed-fetch treatment with optional retry |
| `Avatar` / `AvatarFallback` | Radix-based, initials fallback |
| `Input` | Text input with focus ring |
| `Switch` / `SwitchRow` | Radix-based toggle, used in Settings |
| `Table` / `TableHeader` / `TableRow` / `TableHead` / `TableCell` | Semantic table primitives |
| `Sparkline` | Minimal inline SVG trend line (no charting library dependency) |
| `BarChart` | Minimal horizontal bar chart, same rationale |
| `Modal` / `ModalContent` / `ModalTrigger` / `ModalClose` | Radix Dialog — focus trap, Escape-to-close, `aria-modal` |
| `DropdownMenu` family | Radix Dropdown Menu — used for notifications and the user menu |
| `Tooltip` family | Radix Tooltip — used for collapsed-sidebar labels |

Dashboard-specific components (`components/dashboard/`) compose these
primitives with mock data; layout chrome (`components/layout/`) owns
the sidebar, top bar, and page structure.

## Accessibility (WCAG basics covered)

- Every icon-only control has an `aria-label`.
- Focus is always visible (`focus-visible:ring-2 focus-visible:ring-signal`
  applied globally in `globals.css`, plus per-component where needed).
- Modals, dropdowns, and tooltips use Radix primitives, which handle
  focus trapping, `Escape` to close, and correct ARIA roles.
- The sidebar's active link sets `aria-current="page"`.
- A "Skip to content" link is the first focusable element on every
  page (visually hidden until focused).
- Color is never the only signal — status badges pair color with text
  (`reading`, `high priority`), progress bars expose `aria-valuenow`.
- Reduced motion is respected (`prefers-reduced-motion` shortens all
  animation/transition durations to near-zero in `globals.css`).

This is a foundation, not a full audit — a dedicated accessibility pass
(screen reader testing, color contrast verification against WCAG AA
thresholds) should happen before this ships to real users.

## Performance

- Every route (`app/<route>/page.tsx`) is automatically code-split by
  Next.js's App Router — no manual `dynamic()` wrapping needed for
  route-level lazy loading.
- Server Components by default; `"use client"` is only added where
  interactivity requires it (sidebar, dropdowns, forms, the AI
  Assistant page) — everything else ships zero client JS.
- Charts are hand-rolled SVG (`Sparkline`, `BarChart`) instead of a
  charting library, avoiding a dependency that would dominate bundle
  size for what is currently mock data.

## Future integration points

| Mock data export (`src/data/mock.ts`) | Future source |
| --- | --- |
| `RECENT_PAPERS`, `SAVED_PAPERS` | `GET /api/v1/papers` |
| `TRENDING_TOPICS` | `GET /api/v1/topics/trending` |
| `AI_INSIGHTS` | `GET /api/v1/ai/insights` (backed by `app/ai/provider.py`) |
| `UPCOMING_TASKS` | `GET /api/v1/tasks` |
| `RECENT_CONVERSATIONS`, AI Assistant transcript | `GET /api/v1/ai/conversations` |
| `RESEARCH_ACTIVITY` | `GET /api/v1/users/me/activity` |
| `READING_PROGRESS` | `GET /api/v1/users/me/reading-stats` |
| `NOTIFICATIONS` | `GET /api/v1/notifications` |
| `CURRENT_USER` | `GET /api/v1/users/me` (once auth lands) |
| `UploadPaperModal` submit handler | `POST /api/v1/papers` (multipart upload) |

Every mock export is shaped to match its future response so swapping a
`const x = MOCK_X` for a `useQuery` call is a one-line change per
component, not a rewrite. All twelve sidebar destinations beyond the
dashboard already exist as routes (`app/<route>/page.tsx`) with
consistent `PageHeader` + `EmptyState` or working mock UI — new feature
work replaces the `EmptyState` body, it doesn't restructure the route.
