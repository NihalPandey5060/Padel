import Link from "next/link"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { getCourt } from "@/lib/api"

export default async function CourtDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const court = await getCourt(id)

  return (
    <div className="mx-auto w-full max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
      <Card>
        <CardHeader>
          <Badge>{court.city}</Badge>
          <CardTitle className="mt-2 text-3xl">{court.name}</CardTitle>
          <CardDescription>{court.address}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="leading-7 text-slate-600">{court.description}</p>
          <div className="grid gap-4 sm:grid-cols-2">
            <div><span className="text-sm text-slate-500">Price</span><p className="text-lg font-medium">₹{court.hourly_price}/hr</p></div>
            <div><span className="text-sm text-slate-500">Rating</span><p className="text-lg font-medium">{court.google_rating}</p></div>
            <div><span className="text-sm text-slate-500">Phone</span><p className="text-lg font-medium">{court.phone}</p></div>
            <div><span className="text-sm text-slate-500">Website</span><p className="text-lg font-medium"><a className="text-emerald-700 underline" href={court.website} target="_blank" rel="noreferrer">Open site</a></p></div>
          </div>
          <Link href="/courts"><Button variant="secondary">Back to courts</Button></Link>
        </CardContent>
      </Card>
    </div>
  )
}
