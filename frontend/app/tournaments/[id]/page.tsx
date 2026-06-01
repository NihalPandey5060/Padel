import Link from "next/link"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { getTournament } from "@/lib/api"

export default async function TournamentDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const tournament = await getTournament(id)

  return (
    <div className="mx-auto w-full max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
      <Card>
        <CardHeader>
          <Badge>{tournament.city}</Badge>
          <CardTitle className="mt-2 text-3xl">{tournament.title}</CardTitle>
          <CardDescription>{tournament.venue}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="leading-7 text-slate-600">{tournament.description}</p>
          <div className="grid gap-4 sm:grid-cols-2">
            <div><span className="text-sm text-slate-500">Date</span><p className="text-lg font-medium">{new Date(tournament.date).toLocaleDateString("en-IN")}</p></div>
            <div><span className="text-sm text-slate-500">Entry fee</span><p className="text-lg font-medium">₹{tournament.entry_fee}</p></div>
            <div><span className="text-sm text-slate-500">Registration</span><p className="text-lg font-medium"><a className="text-emerald-700 underline" href={tournament.registration_url} target="_blank" rel="noreferrer">Open link</a></p></div>
          </div>
          <Link href="/tournaments"><Button variant="secondary">Back to tournaments</Button></Link>
        </CardContent>
      </Card>
    </div>
  )
}
