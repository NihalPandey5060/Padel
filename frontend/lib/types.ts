export type Court = {
  id: number
  name: string
  address: string
  city: string
  state: string
  latitude: string
  longitude: string
  hourly_price: number
  phone: string
  website: string
  google_rating: string
  description: string
  created_at: string
  updated_at: string
}

export type Coach = {
  id: number
  name: string
  city: string
  experience_years: number
  specialties: string
  specialties_list: string[]
  phone: string
  bio: string
  verified: boolean
  created_at: string
}

export type Tournament = {
  id: number
  title: string
  city: string
  venue: string
  date: string
  entry_fee: number
  description: string
  registration_url: string
}

export type PagedResponse<T> = {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export type SearchFilters = {
  city?: string
  max_price?: number
  min_experience_years?: number
  verified?: boolean
  specialties?: string[]
  date_from?: string
  date_to?: string
  category?: "courts" | "coaches" | "tournaments" | "all"
  text?: string
}

export type SearchResponse = {
  query: string
  filters: SearchFilters
  results: Array<
    | ({ type: "court" } & Court)
    | ({ type: "coach" } & Coach)
    | ({ type: "tournament" } & Tournament)
  >
  count: number
  page: number
  page_size: number
  has_next: boolean
  has_previous: boolean
  response_time_ms: number
  search_log: { id: number; query: string; response_time_ms: number; created_at: string }
}
