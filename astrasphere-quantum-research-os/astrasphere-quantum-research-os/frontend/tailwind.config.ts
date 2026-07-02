import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        astra: {
          950: '#05060f',
          900: '#0a0e1f',
          800: '#111834',
          700: '#1c2750',
          500: '#4a5bd0',
          400: '#6c7ef0',
          300: '#9aa5f7',
        },
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-mono)', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
};

export default config;
