export interface BarChartDatum {
  label: string;
  value: number;
}

/**
 * Minimal horizontal bar chart, raw SVG/divs — no charting library
 * dependency for what is, in this phase, mock data. Swap for a real
 * charting library alongside real time-series data later if needed.
 */
export function BarChart({ data, className }: { data: BarChartDatum[]; className?: string }) {
  const max = Math.max(...data.map((d) => d.value), 1);

  return (
    <ul className={className} role="img" aria-label="Bar chart">
      {data.map((d) => (
        <li key={d.label} className="mb-3 last:mb-0">
          <div className="mb-1 flex items-baseline justify-between text-body-sm">
            <span className="text-foreground">{d.label}</span>
            <span className="font-mono text-data text-foreground-muted">{d.value}</span>
          </div>
          <div className="h-1.5 w-full overflow-hidden rounded-pill bg-ink-raised">
            <div
              className="h-full rounded-pill bg-entangled"
              style={{ width: `${(d.value / max) * 100}%` }}
            />
          </div>
        </li>
      ))}
    </ul>
  );
}
