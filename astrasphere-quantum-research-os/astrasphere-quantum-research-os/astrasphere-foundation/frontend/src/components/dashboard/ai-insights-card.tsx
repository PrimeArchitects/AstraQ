import { Sparkles } from "lucide-react";

import { DashboardCard } from "@/components/dashboard/dashboard-card";
import { Badge } from "@/components/ui/badge";
import { AI_INSIGHTS, type AIInsight } from "@/data/mock";

const CONFIDENCE_VARIANT: Record<AIInsight["confidence"], "success" | "warning" | "neutral"> = {
  high: "success",
  medium: "warning",
  low: "neutral",
};

/**
 * Surfaces AI-generated observations about the user's library. Purely
 * presentational mock content — no model call happens here. Will source
 * from GET /ai/insights once the AI provider (app/ai/provider.py) is live.
 */
export function AIInsightsCard() {
  return (
    <DashboardCard title="AI Insights" action={{ label: "Open assistant", href: "/ai-assistant" }}>
      <ul className="space-y-4">
        {AI_INSIGHTS.map((insight) => (
          <li key={insight.id} className="flex gap-3">
            <Sparkles className="mt-0.5 h-3.5 w-3.5 shrink-0 text-entangled" aria-hidden />
            <div className="min-w-0">
              <p className="text-body-sm text-foreground">{insight.summary}</p>
              <div className="mt-1.5 flex items-center gap-2">
                <Badge variant={CONFIDENCE_VARIANT[insight.confidence]}>
                  {insight.confidence} confidence
                </Badge>
                <span className="truncate text-body-sm text-foreground-faint">
                  {insight.relatedPaper}
                </span>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </DashboardCard>
  );
}
