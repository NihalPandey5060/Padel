import type { Metadata } from "next"
import { Manrope, Space_Grotesk } from "next/font/google"

import { SiteFooter } from "@/components/site-footer"
import { SiteHeader } from "@/components/site-header"

import "./globals.css"

const display = Space_Grotesk({ subsets: ["latin"], variable: "--font-display" })
const body = Manrope({ subsets: ["latin"], variable: "--font-body" })

export const metadata: Metadata = {
  title: "Padel Discovery AI",
  description: "Discover courts, coaches, and tournaments with filters and AI search.",
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${display.variable} ${body.variable} font-body text-slate-900`}>
        <SiteHeader />
        <main>{children}</main>
        <SiteFooter />
      </body>
    </html>
  )
}
