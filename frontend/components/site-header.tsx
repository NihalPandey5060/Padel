import Link from "next/link"

import { Button } from "@/components/ui/button"

const nav = [
  { href: "/courts", label: "Courts" },
  { href: "/coaches", label: "Coaches" },
  { href: "/tournaments", label: "Tournaments" },
  { href: "/admin", label: "Admin" },
]

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-30 border-b border-white/60 bg-[rgba(251,251,246,0.8)] backdrop-blur-xl">
      <div className="mx-auto flex w-full max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <Link href="/" className="flex flex-col">
          <span className="font-display text-xl font-semibold tracking-tight text-slate-950">Padel Discovery AI</span>
          <span className="text-xs uppercase tracking-[0.28em] text-slate-500">Court, coach, and tournament discovery</span>
        </Link>
        <nav className="hidden items-center gap-2 md:flex">
          {nav.map((item) => (
            <Link key={item.href} href={item.href}>
              <Button variant="ghost" size="sm">
                {item.label}
              </Button>
            </Link>
          ))}
        </nav>
      </div>
    </header>
  )
}
