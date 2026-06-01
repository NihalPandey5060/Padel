import Link from "next/link"

import { SearchForm } from "@/components/search-form"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CoachCard, CourtCard, TournamentCard } from "@/components/entity-cards"
import { searchPadel } from "@/lib/api"

type SearchParams = Record<string, string | string[] | undefined>

function firstValue(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value
}

export default async function SearchPage({ searchParams }: { searchParams: Promise<SearchParams> }) {
  const params = await searchParams
  const query = firstValue(params.q) || ""
  const city = firstValue(params.city)
  const maxPrice = firstValue(params.maxPrice)
  const category = firstValue(params.category)
  const page = Number(firstValue(params.page) || "1")

  const filters = {
    ...(city ? { city } : {}),
    ...(maxPrice ? { max_price: Number(maxPrice) } : {}),
    ...(category ? { category: category as "courts" | "coaches" | "tournaments" | "all" } : {}),
  }

  const results = query ? await searchPadel(query, filters, page, 8) : null

  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="space-y-4">
        <Badge>AI-powered search</Badge>
        <h1 className="font-display text-4xl font-semibold tracking-tight">Search results</h1>
        <p className="max-w-2xl text-slate-600">Tune the filters, submit a natural language query, and the backend will resolve it into safe ORM filters.</p>
      </div>

      <div className="mt-6">
        <SearchForm defaultValue={query} />
      </div>

      <form className="mt-5 grid gap-3 rounded-[28px] border border-slate-200 bg-white p-4 shadow-sm sm:grid-cols-4" action="/search" method="get">
        <input type="hidden" name="q" value={query} />
        <input name="city" defaultValue={city || ""} placeholder="City" className="h-11 rounded-full border border-slate-200 px-4 text-sm outline-none focus:border-emerald-500" />
        <input name="maxPrice" defaultValue={maxPrice || ""} placeholder="Max price" inputMode="numeric" className="h-11 rounded-full border border-slate-200 px-4 text-sm outline-none focus:border-emerald-500" />
        <select name="category" defaultValue={category || "all"} className="h-11 rounded-full border border-slate-200 px-4 text-sm outline-none focus:border-emerald-500">
          <option value="all">All</option>
          <option value="courts">Courts</option>
          <option value="coaches">Coaches</option>
          <option value="tournaments">Tournaments</option>
        </select>
        <Button type="submit">Apply filters</Button>
      </form>

      {!query ? (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Try a search</CardTitle>
            <CardDescription>Examples: beginner courts in Bangalore under ₹800, good coaches near Whitefield, weekend tournaments in Bangalore.</CardDescription>
          </CardHeader>
        </Card>
      ) : null}

      {results ? (
        <div className="mt-8 space-y-8">
          <Card>
            <CardHeader>
              <CardTitle>Search summary</CardTitle>
              <CardDescription>{results.count} results found in {results.response_time_ms}ms</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-wrap gap-2">
              {Object.entries(results.filters).map(([key, value]) => (
                <Badge key={key} className="border-slate-200 bg-slate-100 text-slate-700">{key}: {Array.isArray(value) ? value.join(", ") : String(value)}</Badge>
              ))}
            </CardContent>
          </Card>

          {results.results.some((item) => item.type === "court") ? (
            <section className="space-y-4">
              <h2 className="font-display text-2xl font-semibold">Courts</h2>
              <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
                {results.results
                  .filter((item): item is Extract<(typeof results.results)[number], { type: "court" }> => item.type === "court")
                  .map((court) => <CourtCard key={court.id} court={court} />)}
              </div>
            </section>
          ) : null}

          {results.results.some((item) => item.type === "coach") ? (
            <section className="space-y-4">
              <h2 className="font-display text-2xl font-semibold">Coaches</h2>
              <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
                {results.results
                  .filter((item): item is Extract<(typeof results.results)[number], { type: "coach" }> => item.type === "coach")
                  .map((coach) => <CoachCard key={coach.id} coach={coach} />)}
              </div>
            </section>
          ) : null}

          {results.results.some((item) => item.type === "tournament") ? (
            <section className="space-y-4">
              <h2 className="font-display text-2xl font-semibold">Tournaments</h2>
              <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
                {results.results
                  .filter((item): item is Extract<(typeof results.results)[number], { type: "tournament" }> => item.type === "tournament")
                  .map((tournament) => <TournamentCard key={tournament.id} tournament={tournament} />)}
              </div>
            </section>
          ) : null}

          <div className="flex items-center justify-between">
            <span className="text-sm text-slate-600">Page {page}</span>
            <div className="flex gap-2">
              {page > 1 ? (
                <Link href={{ pathname: "/search", query: { q: query, city, maxPrice, category, page: page - 1 } }}>
                  <Button variant="secondary" size="sm">Previous</Button>
                </Link>
              ) : null}
              {results.count > page * 8 ? (
                <Link href={{ pathname: "/search", query: { q: query, city, maxPrice, category, page: page + 1 } }}>
                  <Button variant="secondary" size="sm">Next</Button>
                </Link>
              ) : null}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  )
}
