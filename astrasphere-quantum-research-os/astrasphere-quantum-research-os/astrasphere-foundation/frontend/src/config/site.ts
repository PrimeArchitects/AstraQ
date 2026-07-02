/** Central site metadata and navigation config — single source of truth. */
export const siteConfig = {
  name: "AstraSphere",
  fullName: "AstraSphere Quantum Research OS",
  description:
    "An AI-powered research operating system for quantum computing labs, universities, and R&D teams.",
  nav: [
    { label: "Console", href: "/" },
    { label: "Experiments", href: "/experiments" },
    { label: "Datasets", href: "/datasets" },
    { label: "Publications", href: "/publications" },
  ],
} as const;
