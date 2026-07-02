import type { ResearchProject } from '@/types/research';
import { StatusBadge } from './StatusBadge';

export function ProjectCard({ project }: { project: ResearchProject }) {
  return (
    <article className="rounded-xl border border-astra-700/60 bg-astra-900/60 p-5 shadow-lg shadow-black/20 transition hover:border-astra-500/60">
      <div className="mb-2 flex items-start justify-between gap-3">
        <h3 className="text-base font-semibold text-slate-100">{project.title}</h3>
        <StatusBadge status={project.status} />
      </div>
      <p className="line-clamp-3 text-sm text-slate-400">
        {project.summary || 'No summary provided yet.'}
      </p>
      <p className="mt-4 text-xs text-slate-500">
        Updated {new Date(project.updated_at).toLocaleDateString()}
      </p>
    </article>
  );
}
