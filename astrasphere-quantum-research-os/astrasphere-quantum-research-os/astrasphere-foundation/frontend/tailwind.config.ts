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
          DEFAULT: "rgb(var(--color-ink) / <alpha-value>)",
          panel: "rgb(var(--color-ink-panel) / <alpha-value>)",
          raised: "rgb(var(--color-ink-raised) / <alpha-value>)",
          overlay: "#05070A",
        },
        line: {
          DEFAULT: "rgb(var(--color-line) / <alpha-value>)",
          faint: "rgb(var(--color-line-faint) / <alpha-value>)",
          strong: "rgb(var(--color-line-strong) / <alpha-value>)",
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
          dim: "#A83E4E",
        },
        foreground: {
          DEFAULT: "rgb(var(--color-foreground) / <alpha-value>)",
          muted: "rgb(var(--color-foreground-muted) / <alpha-value>)",
          faint: "rgb(var(--color-foreground-faint) / <alpha-value>)",
        },
        // Semantic aliases — use these in feature/status contexts (badges,
        // alerts) so intent reads clearly; `signal`/`pulse`/`entangled`
        // remain the brand names used in layout chrome and data viz.
        success: {
          DEFAULT: "#4CD6C0",
          subtle: "#173229",
        },
        warning: {
          DEFAULT: "#F4A340",
          subtle: "#332510",
        },
        info: {
          DEFAULT: "#8C85D8",
          subtle: "#211F38",
        },
        critical: {
          DEFAULT: "#E5556B",
          subtle: "#331A20",
        },
      },
      fontFamily: {
        display: ["var(--font-display)", "sans-serif"],
        body: ["var(--font-body)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
      // Typographic scale. Every text size in the console should map to
      // one of these rather than an arbitrary Tailwind size — keeps the
      // hierarchy consistent across dozens of feature pages.
      fontSize: {
        "display-lg": ["2.25rem", { lineHeight: "1.15", letterSpacing: "-0.01em" }],
        "display-md": ["1.75rem", { lineHeight: "1.2", letterSpacing: "-0.01em" }],
        "display-sm": ["1.375rem", { lineHeight: "1.25" }],
        title: ["1.0625rem", { lineHeight: "1.4" }],
        body: ["0.875rem", { lineHeight: "1.6" }],
        "body-sm": ["0.8125rem", { lineHeight: "1.55" }],
        label: ["0.6875rem", { lineHeight: "1.4", letterSpacing: "0.08em" }],
        data: ["0.8125rem", { lineHeight: "1.4" }],
        "data-lg": ["1.75rem", { lineHeight: "1.15" }],
      },
      borderRadius: {
        DEFAULT: "3px",
        panel: "2px",
        control: "4px",
        pill: "999px",
      },
      // Layering contract: reference these instead of ad hoc z-index
      // values so overlays consistently stack above chrome, and chrome
      // consistently stacks above page content.
      zIndex: {
        chrome: "30",
        overlay: "40",
        modal: "50",
        toast: "60",
      },
      boxShadow: {
        panel: "0 1px 0 0 rgba(255,255,255,0.03) inset",
        raised: "0 8px 24px -8px rgba(0,0,0,0.5)",
        glow: "0 0 0 1px rgba(76,214,192,0.25), 0 0 24px -4px rgba(76,214,192,0.35)",
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
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        "overlay-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        "dialog-in": {
          from: { opacity: "0", transform: "translateY(4px) scale(0.98)" },
          to: { opacity: "1", transform: "translateY(0) scale(1)" },
        },
        "slide-in-left": {
          from: { transform: "translateX(-100%)" },
          to: { transform: "translateX(0)" },
        },
        "menu-in": {
          from: { opacity: "0", transform: "translateY(-2px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      animation: {
        coherence: "coherence 3.2s ease-in-out infinite",
        scan: "scan 4s linear infinite",
        "fade-in": "fade-in 0.15s ease-out",
        "overlay-in": "overlay-in 0.15s ease-out",
        "dialog-in": "dialog-in 0.15s ease-out",
        "slide-in-left": "slide-in-left 0.2s ease-out",
        "menu-in": "menu-in 0.12s ease-out",
        shimmer: "shimmer 1.8s linear infinite",
      },
    },
  },
  plugins: [],
};

export default config;
