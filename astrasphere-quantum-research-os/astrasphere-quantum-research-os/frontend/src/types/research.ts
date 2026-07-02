export type ResearchStatus = 'draft' | 'active' | 'completed' | 'archived';

export interface ResearchProject {
  id: string;
  title: string;
  summary: string;
  status: ResearchStatus;
  created_at: string;
  updated_at: string;
}

export interface ResearchProjectCreateInput {
  title: string;
  summary?: string;
  status?: ResearchStatus;
}
