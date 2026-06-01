import Link from "next/link"

import { SearchForm } from "@/components/search-form"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CourtCard, CoachCard, TournamentCard } from "@/components/entity-cards"
import { getCoaches, getCourts, getTournaments } from "@/lib/api"

export default async function HomePage() {
  const [courts, coaches, tournaments] = await Promise.all([getCourts(3), getCoaches(3), getTournaments(3)])

  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <section className="grid gap-8 rounded-[36px] border border-white/70 bg-white/70 p-6 shadow-soft backdrop-blur sm:p-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div className="space-y-6">
          <Badge>Demo-quality padel discovery</Badge>
          <div className="space-y-4">
            <h1 className="font-display text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl lg:text-6xl">
              Find the right padel court, coach, or tournament in seconds.
            </h1>
            <p className="max-w-2xl text-lg leading-8 text-slate-600">
              Search naturally, filter precisely, and browse polished detail pages backed by Django, PostgreSQL, and Gemini-powered filter extraction.
            </p>
          </div>
          <SearchForm />
          <div className="flex flex-wrap gap-3">
            <Link href="/courts"><Button variant="secondary">Browse courts</Button></Link>
            <Link href="/coaches"><Button variant="secondary">Browse coaches</Button></Link>
            <Link href="/tournaments"><Button variant="secondary">Browse tournaments</Button></Link>
          </div>
        </div>
        <Card className="overflow-hidden border-slate-200 bg-slate-950 text-white shadow-soft">
          <CardHeader>
            <CardTitle className="text-white">Natural language examples</CardTitle>
            <CardDescription className="text-slate-300">The backend converts plain English into safe Django ORM filters.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              "Beginner padel courts in Bangalore under ₹800",
              "Good coaches near Whitefield",
              "Weekend tournaments in Bangalore",
            ].map((example) => (
              <div key={example} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-100">
                {example}
              </div>
            ))}
          </CardContent>
        </Card>
      </section>

      <section className="mt-12 space-y-5">
        <div className="flex items-end justify-between gap-4">
          <div>
            <h2 className="font-display text-3xl font-semibold tracking-tight">Featured courts</h2>
            <p className="text-slate-600">A quick view of what is available near major Indian metro areas.</p>
          </div>
          <Link href="/courts"><Button variant="ghost">View all</Button></Link>
        </div>
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {courts.results.map((court) => <CourtCard key={court.id} court={court} />)}
        </div>
      </section>

      <section className="mt-12 grid gap-10 lg:grid-cols-2">
        <div className="space-y-5">
          <div className="flex items-end justify-between gap-4">
            <div>
              <h2 className="font-display text-3xl font-semibold tracking-tight">Featured coaches</h2>
              <p className="text-slate-600">Verified and experienced coaches for different playing styles.</p>
            </div>
            <Link href="/coaches"><Button variant="ghost">View all</Button></Link>
          </div>
          <div className="grid gap-5">
            {coaches.results.map((coach) => <CoachCard key={coach.id} coach={coach} />)}
          </div>
        </div>

        <div className="space-y-5">
          <div className="flex items-end justify-between gap-4">
            <div>
              <h2 className="font-display text-3xl font-semibold tracking-tight">Featured tournaments</h2>
              <p className="text-slate-600">Upcoming events for weekend players and competitive ladders.</p>
            </div>
            <Link href="/tournaments"><Button variant="ghost">View all</Button></Link>
          </div>
          <div className="grid gap-5">
            {tournaments.results.map((tournament) => <TournamentCard key={tournament.id} tournament={tournament} />)}
          </div>
        </div>
      </section>
    </div>
  )
}
