import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AstraSphere Quantum Research OS',
  description: 'A research operations platform for quantum computing teams.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
