/**
 * Mock data for the dashboard UI.
 *
 * Every export here is shaped to match what the eventual API response
 * will look like (see field naming) so swapping a `const x = MOCK_X`
 * for a TanStack Query call later is a one-line change, not a
 * component rewrite. See docs/design-system.md "Integration points"
 * for the mapping from mock export to future endpoint.
 */

export interface Paper {
  id: string;
  title: string;
  authors: string[];
  venue: string;
  year: number;
  status: "reading" | "saved" | "reviewed" | "new";
  progress?: number;
  tags: string[];
}

export const RECENT_PAPERS: Paper[] = [
  {
    id: "p1",
    title: "Fault-Tolerant Logical Qubits on a Neutral-Atom Array",
    authors: ["A. Reyes", "M. Okonkwo"],
    venue: "Nature Physics",
    year: 2026,
    status: "reading",
    progress: 62,
    tags: ["error correction", "neutral atoms"],
  },
  {
    id: "p2",
    title: "Variational Quantum Eigensolvers for Molecular Ground States",
    authors: ["S. Lindqvist", "P. Chen", "R. Haas"],
    venue: "PRX Quantum",
    year: 2025,
    status: "new",
    tags: ["VQE", "chemistry"],
  },
  {
    id: "p3",
    title: "Scalable Surface Code Decoding with Transformer Models",
    authors: ["J. Whitfield"],
    venue: "arXiv preprint",
    year: 2026,
    status: "saved",
    tags: ["decoding", "ML"],
  },
  {
    id: "p4",
    title: "Benchmarking Coherence Times Across Superconducting Architectures",
    authors: ["D. Kowalski", "N. Fujimoto"],
    venue: "Quantum Science and Technology",
    year: 2025,
    status: "reviewed",
    tags: ["benchmarking", "superconducting"],
  },
];

export const SAVED_PAPERS: Paper[] = [
  RECENT_PAPERS[2]!,
  {
    id: "p5",
    title: "Photonic Cluster States for Measurement-Based Computation",
    authors: ["E. Voss"],
    venue: "Physical Review Letters",
    year: 2025,
    status: "saved",
    tags: ["photonics", "MBQC"],
  },
  {
    id: "p6",
    title: "Noise-Adaptive Compilation for NISQ-Era Circuits",
    authors: ["T. Anand", "L. Bergström"],
    venue: "IEEE Quantum Week",
    year: 2026,
    status: "saved",
    tags: ["compilation", "NISQ"],
  },
];

export interface TrendingTopic {
  id: string;
  name: string;
  paperCount: number;
  trend: number[];
  changePct: number;
}

export const TRENDING_TOPICS: TrendingTopic[] = [
  {
    id: "t1",
    name: "Error Correction",
    paperCount: 342,
    trend: [12, 18, 15, 22, 28, 31, 40],
    changePct: 18,
  },
  {
    id: "t2",
    name: "Neutral Atom Arrays",
    paperCount: 187,
    trend: [8, 9, 14, 13, 19, 24, 26],
    changePct: 24,
  },
  {
    id: "t3",
    name: "Quantum Machine Learning",
    paperCount: 265,
    trend: [20, 19, 23, 21, 25, 27, 24],
    changePct: 6,
  },
  {
    id: "t4",
    name: "Photonic Computing",
    paperCount: 129,
    trend: [6, 7, 6, 9, 11, 10, 14],
    changePct: 12,
  },
];

export interface AIInsight {
  id: string;
  summary: string;
  relatedPaper: string;
  confidence: "high" | "medium" | "low";
}

export const AI_INSIGHTS: AIInsight[] = [
  {
    id: "i1",
    summary:
      "Three papers in your library report conflicting coherence-time baselines for the same qubit architecture — worth a comparison pass.",
    relatedPaper: "Benchmarking Coherence Times Across Superconducting Architectures",
    confidence: "high",
  },
  {
    id: "i2",
    summary:
      "This decoding approach shares its loss formulation with a 2024 paper already in your saved list.",
    relatedPaper: "Scalable Surface Code Decoding with Transformer Models",
    confidence: "medium",
  },
  {
    id: "i3",
    summary: "A new preprint cites your team's 2025 VQE benchmark as its primary baseline.",
    relatedPaper: "Variational Quantum Eigensolvers for Molecular Ground States",
    confidence: "high",
  },
];

export interface Task {
  id: string;
  title: string;
  due: string;
  priority: "low" | "medium" | "high";
  done: boolean;
}

export const UPCOMING_TASKS: Task[] = [
  {
    id: "task1",
    title: "Review decoding transformer preprint",
    due: "Today",
    priority: "high",
    done: false,
  },
  {
    id: "task2",
    title: "Prepare literature summary for team sync",
    due: "Tomorrow",
    priority: "medium",
    done: false,
  },
  {
    id: "task3",
    title: "Reply to co-author comments on VQE draft",
    due: "Fri",
    priority: "medium",
    done: false,
  },
  { id: "task4", title: "Archive Q1 reading list", due: "Next week", priority: "low", done: true },
];

export interface Conversation {
  id: string;
  title: string;
  lastMessage: string;
  updatedAt: string;
}

export const RECENT_CONVERSATIONS: Conversation[] = [
  {
    id: "c1",
    title: "Surface code decoder comparison",
    lastMessage:
      "Here's how the transformer approach compares to belief propagation on distance-11 codes...",
    updatedAt: "10m ago",
  },
  {
    id: "c2",
    title: "VQE ansatz selection",
    lastMessage:
      "For this molecule size, a hardware-efficient ansatz will likely outperform UCCSD given your qubit budget.",
    updatedAt: "2h ago",
  },
  {
    id: "c3",
    title: "Coherence benchmark discrepancy",
    lastMessage:
      "The gap is likely explained by differing T2* measurement protocols between the two groups.",
    updatedAt: "Yesterday",
  },
];

export interface ActivityEvent {
  id: string;
  type: "upload" | "comment" | "save" | "ai" | "team";
  description: string;
  timestamp: string;
}

export const RESEARCH_ACTIVITY: ActivityEvent[] = [
  {
    id: "a1",
    type: "upload",
    description: "You uploaded \u201cFault-Tolerant Logical Qubits on a Neutral-Atom Array\u201d",
    timestamp: "09:41",
  },
  {
    id: "a2",
    type: "ai",
    description: "AI Assistant generated 3 insights on your saved papers",
    timestamp: "09:15",
  },
  {
    id: "a3",
    type: "comment",
    description: "M. Okonkwo commented on your VQE draft",
    timestamp: "Yesterday, 17:02",
  },
  {
    id: "a4",
    type: "save",
    description: "You saved \u201cPhotonic Cluster States for Measurement-Based Computation\u201d",
    timestamp: "Yesterday, 14:20",
  },
  {
    id: "a5",
    type: "team",
    description: "R. Haas added you to \u201cDecoding Benchmarks\u201d workspace",
    timestamp: "2 days ago",
  },
];

export const READING_PROGRESS = {
  papersInProgress: 4,
  weeklyGoal: 8,
  papersReadThisWeek: 5,
  streakDays: 6,
};

export interface QuickAction {
  id: string;
  title: string;
  description: string;
  href?: string;
}

export const QUICK_ACTIONS: QuickAction[] = [
  {
    id: "qa1",
    title: "Upload Research Paper",
    description: "Add a PDF to your library for AI-assisted analysis.",
  },
  {
    id: "qa2",
    title: "Compare Papers",
    description: "Run a side-by-side comparison of methods and results.",
    href: "/paper-comparison",
  },
  {
    id: "qa3",
    title: "Open AI Chat",
    description: "Ask questions grounded in your research library.",
    href: "/ai-assistant",
  },
  {
    id: "qa4",
    title: "Explore Equations",
    description: "Look up and derive quantum formalism interactively.",
    href: "/equation-explorer",
  },
  {
    id: "qa5",
    title: "Build Quantum Circuit",
    description: "Sketch and simulate a circuit visually.",
    href: "/circuit-builder",
  },
  {
    id: "qa6",
    title: "View Literature Graph",
    description: "See how your library connects citation-to-citation.",
    href: "/literature-graph",
  },
];

export const NOTIFICATIONS = [
  { id: "n1", title: "New citation of your VQE benchmark", time: "5m ago", unread: true },
  { id: "n2", title: "M. Okonkwo replied to your comment", time: "1h ago", unread: true },
  { id: "n3", title: "Weekly reading digest is ready", time: "Yesterday", unread: false },
];

export const CURRENT_USER = {
  name: "Dr. Elena Vasquez",
  email: "e.vasquez@astrasphere.io",
  initials: "EV",
  role: "Quantum Error Correction Lab",
};
