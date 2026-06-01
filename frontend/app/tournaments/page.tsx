import Link from "next/link"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { TournamentCard } from "@/components/entity-cards"
import { getTournaments } from "@/lib/api"

export default async function TournamentsPage() {
  const tournaments = await getTournaments(24)

  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="space-y-4">
        <Badge>Tournaments</Badge>
        <h1 className="font-display text-4xl font-semibold tracking-tight">Browse tournaments</h1>
        <p className="max-w-2xl text-slate-600">Find weekend events, ladders, and competition formats.</p>
      </div>
      <div className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {tournaments.results.map((tournament) => <TournamentCard key={tournament.id} tournament={tournament} />)}
      </div>
      <div className="mt-8">
        <Link href="/search"><Button variant="secondary">Search with filters</Button></Link>
      </div>
    </div>
  )
}
