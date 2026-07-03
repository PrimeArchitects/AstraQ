"use client";

import { Sparkles } from "lucide-react";

import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Panel } from "@/components/ui/panel";
import { RECENT_CONVERSATIONS } from "@/data/mock";

// Static mock transcript for the active conversation — no model call
// happens on this page. Wire this to app/ai/provider.py::AIProvider.complete
// once that's implemented.
const MOCK_TRANSCRIPT = [
  {
    role: "user" as const,
    text: "How does the transformer decoder compare to belief propagation on distance-11 surface codes?",
  },
  {
    role: "assistant" as const,
    text: "Based on the benchmark in your library, the transformer decoder achieves a lower logical error rate at distance 11, but belief propagation remains faster per-shot. The gap narrows as code distance increases.",
  },
];

export default function AIAssistantPage() {
  return (
    <AppShell>
      <div className="mx-auto flex h-full max-w-6xl gap-6">
        <aside className="hidden w-64 shrink-0 flex-col gap-2 lg:flex">
          <p className="mb-1 font-mono text-label uppercase tracking-widest text-foreground-faint">
            Conversations
          </p>
          {RECENT_CONVERSATIONS.map((c, i) => (
            <button
              key={c.id}
              className={`w-full rounded-control px-3 py-2 text-left text-body-sm transition-colors ${
                i === 0
                  ? "bg-ink-raised text-signal"
                  : "text-foreground-muted hover:bg-ink-raised hover:text-foreground"
              }`}
            >
              <p className="truncate">{c.title}</p>
              <p className="mt-0.5 truncate font-mono text-label text-foreground-faint">
                {c.updatedAt}
              </p>
            </button>
          ))}
        </aside>

        <div className="flex flex-1 flex-col">
          <PageHeader
            title="AI Assistant"
            description="Ask questions grounded in your research library."
          />
          <Panel className="flex flex-1 flex-col gap-4 overflow-y-auto">
            {MOCK_TRANSCRIPT.map((message, i) => (
              <div key={i} className={`flex gap-3 ${message.role === "user" ? "justify-end" : ""}`}>
                {message.role === "assistant" && (
                  <Sparkles className="mt-1 h-4 w-4 shrink-0 text-entangled" aria-hidden />
                )}
                <p
                  className={`max-w-lg text-body-sm ${
                    message.role === "user"
                      ? "rounded-control bg-ink-raised px-3 py-2 text-foreground"
                      : "text-foreground-muted"
                  }`}
                >
                  {message.text}
                </p>
              </div>
            ))}
          </Panel>
          <form className="mt-4 flex gap-2" onSubmit={(e) => e.preventDefault()}>
            <Input
              placeholder="Ask about your research library..."
              aria-label="Message the AI Assistant"
            />
            <Button type="submit">Send</Button>
          </form>
        </div>
      </div>
    </AppShell>
  );
}
