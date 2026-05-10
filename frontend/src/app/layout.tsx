import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Text Summarizer",
  description: "Summarize text and PDFs using AI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 font-sans">
        {children}
      </body>
    </html>
  );
}
