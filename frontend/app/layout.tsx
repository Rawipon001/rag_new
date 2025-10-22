import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'AI Tax Advisor - ผู้ช่วยวางแผนภาษีอัจฉริยะ',
  description: 'ระบบวางแผนภาษีเงินได้บุคคลธรรมดาด้วย AI พร้อมคำแนะนำวิธีลดภาษีอย่างชาญฉลาด',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="th">
      <body className={inter.className}>{children}</body>
    </html>
  );
}