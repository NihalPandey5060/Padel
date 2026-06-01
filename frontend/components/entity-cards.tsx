import Link from "next/link"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import type { Coach, Court, Tournament } from "@/lib/types"

export function CourtCard({ court }: { court: Court }) {
  return (
    <Card className="h-full">
      <CardHeader>
        <div className="mb-3 flex items-center justify-between gap-3">
          <Badge>{court.city}</Badge>
          <span className="text-sm font-medium text-slate-700">₹{court.hourly_price}/hr</span>
        </div>
        <CardTitle>{court.name}</CardTitle>
        <CardDescription>{court.address}</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <p className="line-clamp-3 text-sm leading-6 text-slate-600">{court.description}</p>
        <div className="flex items-center justify-between gap-3">
          <span className="text-sm text-slate-500">Rating {court.google_rating}</span>
          <Link href={`/courts/${court.id}`}>
            <Button variant="secondary" size="sm">View details</Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  )
}

export function CoachCard({ coach }: { coach: Coach }) {
  return (
    <Card className="h-full">
      <CardHeader>
        <div className="mb-3 flex items-center justify-between gap-3">
          <Badge>{coach.city}</Badge>
          {coach.verified ? <Badge className="border-emerald-200 bg-emerald-100 text-emerald-900">Verified</Badge> : null}
        </div>
        <CardTitle>{coach.name}</CardTitle>
        <CardDescription>{coach.experience_years} years experience</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <p className="line-clamp-3 text-sm leading-6 text-slate-600">{coach.bio}</p>
        <div className="flex flex-wrap gap-2">
          {coach.specialties_list.map((specialty) => (
            <Badge key={specialty} className="bg-slate-100 text-slate-700 border-slate-200">{specialty}</Badge>
          ))}
        </div>
        <div className="flex items-center justify-between gap-3">
          <span className="text-sm text-slate-500">Specialties</span>
          <Link href={`/coaches/${coach.id}`}>
            <Button variant="secondary" size="sm">View profile</Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  )
}

export function TournamentCard({ tournament }: { tournament: Tournament }) {
  return (
    <Card className="h-full">
      <CardHeader>
        <div className="mb-3 flex items-center justify-between gap-3">
          <Badge>{tournament.city}</Badge>
          <span className="text-sm font-medium text-slate-700">₹{tournament.entry_fee}</span>
        </div>
        <CardTitle>{tournament.title}</CardTitle>
        <CardDescription>{new Date(tournament.date).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })}</CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <p className="line-clamp-3 text-sm leading-6 text-slate-600">{tournament.description}</p>
        <div className="flex items-center justify-between gap-3">
          <span className="text-sm text-slate-500">{tournament.venue}</span>
          <Link href={`/tournaments/${tournament.id}`}>
            <Button variant="secondary" size="sm">View event</Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  )
}
