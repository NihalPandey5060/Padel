import { Search } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function SearchForm({ defaultValue }: { defaultValue?: string }) {
  return (
    <form action="/search" method="get" className="flex w-full flex-col gap-3 rounded-[28px] border border-slate-200 bg-white p-3 shadow-soft sm:flex-row">
      <div className="relative flex-1">
        <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
        <Input name="q" defaultValue={defaultValue} placeholder="Beginner padel courts in Bangalore under ₹800" className="pl-10" />
      </div>
      <Button type="submit">Search</Button>
    </form>
  )
}
