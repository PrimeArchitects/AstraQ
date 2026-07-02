/** Route-level loading UI — Next.js renders this automatically during navigation/data fetch. */
export default function Loading() {
  return (
    <div className="flex h-screen items-center justify-center bg-ink">
      <div className="flex flex-col items-center gap-4">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-line border-t-signal" />
        <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-foreground-faint">
          Calibrating
        </p>
      </div>
    </div>
  );
}
