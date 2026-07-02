import type { Config } from "tailwindcss";

/**
 * Design tokens for the AstraSphere console UI.
 *
 * The palette and type scale come from the product's visual language —
 * an instrument-panel aesthetic (cryostat blacks, phosphor-signal accent,
 * monospace data readouts) rather than generic dashboard defaults.
 * Extend this file when adding new tokens; avoid ad hoc hex values in
 * components.
 */
const config: Config = {
  darkMode: ["class"],
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#0A0D12",
          panel: "#10141C",
          raised: "#161B25",
        },
        line: {
          DEFAULT: "#232A36",
          faint: "#181E28",
        },
        signal: {
          DEFAULT: "#4CD6C0",
          dim: "#2F8F82",
          bright: "#7FF2E0",
        },
        pulse: {
          DEFAULT: "#F4A340",
          dim: "#B97A2E",
        },
        entangled: {
          DEFAULT: "#8C85D8",
          dim: "#615BA0",
        },
        danger: {
          DEFAULT: "#E5556B",
        },
        foreground: {
          DEFAULT: "#E7EBF2",
          muted: "#8C96A8",
          faint: "#5A6478",
        },
      },
      fontFamily: {
        display: ["var(--font-display)", "sans-serif"],
        body: ["var(--font-body)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
      borderRadius: {
        DEFAULT: "3px",
        panel: "2px",
      },
      keyframes: {
        coherence: {
          "0%, 100%": { opacity: "0.35", transform: "scale(0.98)" },
          "50%": { opacity: "1", transform: "scale(1.02)" },
        },
        scan: {
          "0%": { transform: "translateY(-100%)" },
          "100%": { transform: "translateY(100%)" },
        },
      },
      animation: {
        coherence: "coherence 3.2s ease-in-out infinite",
        scan: "scan 4s linear infinite",
      },
    },
  },
  plugins: [],
};

export default config;
