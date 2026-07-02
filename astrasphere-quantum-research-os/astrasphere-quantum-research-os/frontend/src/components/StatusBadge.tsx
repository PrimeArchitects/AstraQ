import type { ResearchStatus } from '@/types/research';

const STATUS_STYLES: Record<ResearchStatus, string> = {
  draft: 'bg-slate-700 text-slate-200',
  active: 'bg-emerald-600/20 text-emerald-300 ring-1 ring-emerald-500/40',
  completed: 'bg-astra-500/20 text-astra-300 ring-1 ring-astra-400/40',
  archived: 'bg-slate-800 text-slate-400',
};

export function StatusBadge({ status }: { status: ResearchStatus }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize ${STATUS_STYLES[status]}`}
    >
      {status}
    </span>
  );
}
