import type { ResearchProject, ResearchProjectCreateInput } from '@/types/research';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1';

class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...init?.headers,
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new ApiError(detail || response.statusText, response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export const api = {
  health: () => request<{ status: string }>('/health'),

  listProjects: () => request<ResearchProject[]>('/research'),

  getProject: (id: string) => request<ResearchProject>(`/research/${id}`),

  createProject: (input: ResearchProjectCreateInput) =>
    request<ResearchProject>('/research', {
      method: 'POST',
      body: JSON.stringify(input),
    }),

  deleteProject: (id: string) =>
    request<void>(`/research/${id}`, {
      method: 'DELETE',
    }),
};

export { ApiError };
