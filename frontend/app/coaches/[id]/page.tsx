import Link from "next/link"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { getCoach } from "@/lib/api"

export default async function CoachDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const coach = await getCoach(id)

  const specialties = coach.specialties.split(",").map((item) => item.trim()).filter(Boolean)

  return (
    <div className="mx-auto w-full max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
      <Card>
        <CardHeader>
          <Badge>{coach.city}</Badge>
          <CardTitle className="mt-2 text-3xl">{coach.name}</CardTitle>
          <CardDescription>{coach.experience_years} years experience</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="leading-7 text-slate-600">{coach.bio}</p>
          <div className="flex flex-wrap gap-2">
            {specialties.map((specialty) => <Badge key={specialty} className="bg-slate-100 text-slate-700 border-slate-200">{specialty}</Badge>)}
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <div><span className="text-sm text-slate-500">Phone</span><p className="text-lg font-medium">{coach.phone}</p></div>
            <div><span className="text-sm text-slate-500">Verified</span><p className="text-lg font-medium">{coach.verified ? "Yes" : "No"}</p></div>
          </div>
          <Link href="/coaches"><Button variant="secondary">Back to coaches</Button></Link>
        </CardContent>
      </Card>
    </div>
  )
}
