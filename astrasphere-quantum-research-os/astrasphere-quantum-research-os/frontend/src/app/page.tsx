import { ProjectCard } from '@/components/ProjectCard';
import { api, ApiError } from '@/lib/api';
import type { ResearchProject } from '@/types/research';

async function getProjects(): Promise<{ projects: ResearchProject[]; error?: string }> {
  try {
    const projects = await api.listProjects();
    return { projects };
  } catch (err) {
    const message = err instanceof ApiError ? err.message : 'Unable to reach the backend API.';
    return { projects: [], error: message };
  }
}

export default async function HomePage() {
  const { projects, error } = await getProjects();

  return (
    <main className="mx-auto max-w-5xl px-6 py-16">
      <header className="mb-12">
        <p className="mb-2 text-sm font-medium uppercase tracking-widest text-astra-400">
          AstraSphere
        </p>
        <h1 className="text-3xl font-bold text-slate-50 sm:text-4xl">
          Quantum Research Operating System
        </h1>
        <p className="mt-3 max-w-2xl text-slate-400">
          Coordinate research projects, semantic search over your literature corpus, and experiment
          tracking from a single control plane.
        </p>
      </header>

      <section>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-200">Research Projects</h2>
          <span className="text-sm text-slate-500">{projects.length} total</span>
        </div>

        {error ? (
          <div className="rounded-lg border border-amber-500/30 bg-amber-500/10 p-4 text-sm text-amber-300">
            {error} — start the backend with <code className="font-mono">docker compose up</code> to
            populate this list.
          </div>
        ) : projects.length === 0 ? (
          <div className="rounded-lg border border-dashed border-astra-700 p-8 text-center text-slate-500">
            No research projects yet. Create one via the API to see it here.
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {projects.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
