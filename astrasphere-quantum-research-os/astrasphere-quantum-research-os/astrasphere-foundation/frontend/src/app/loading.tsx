import { Skeleton } from "@/components/ui/skeleton";

/** Route-level loading UI, shaped like the dashboard so it doesn't "pop" on load. */
export default function Loading() {
  return (
    <div className="flex h-screen bg-ink">
      <div className="hidden w-64 shrink-0 border-r border-line md:block" />
      <div className="flex-1 p-6 lg:p-10">
        <div className="mx-auto flex max-w-7xl flex-col gap-8">
          <div className="flex items-center justify-between border-b border-line pb-8">
            <div className="space-y-2">
              <Skeleton className="h-3 w-24" />
              <Skeleton className="h-8 w-64" />
            </div>
            <Skeleton className="h-24 w-24 rounded-full" />
          </div>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <Skeleton key={i} className="h-24" />
            ))}
          </div>
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
            <Skeleton className="h-64 lg:col-span-2" />
            <Skeleton className="h-64" />
          </div>
        </div>
      </div>
    </div>
  );
}
