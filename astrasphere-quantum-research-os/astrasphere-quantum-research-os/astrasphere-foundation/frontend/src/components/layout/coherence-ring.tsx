/**
 * Signature visual: a pulsing ring evoking a qubit's coherence readout.
 * This is the one deliberately expressive element on the placeholder
 * dashboard — everything else stays quiet so this reads clearly.
 */
export function CoherenceRing() {
  return (
    <div className="relative flex h-40 w-40 items-center justify-center" aria-hidden>
      <div className="absolute h-full w-full animate-coherence rounded-full border border-signal/40" />
      <div className="absolute h-28 w-28 animate-coherence rounded-full border border-entangled/30 [animation-delay:0.6s]" />
      <div className="h-2 w-2 rounded-full bg-signal shadow-[0_0_16px_theme(colors.signal.DEFAULT)]" />
    </div>
  );
}
