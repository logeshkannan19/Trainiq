import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Trainiq Fit - AI Personal Trainer on WhatsApp',
  description: 'Your AI-powered personal fitness coach delivered daily to WhatsApp. Get personalized workout plans, diet recommendations, and real-time motivation.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-900 text-white antialiased">{children}</body>
    </html>
  );
}
