import type { Coach, Court, PagedResponse, SearchFilters, SearchResponse, Tournament } from "@/lib/types"

function getApiBaseUrl() {
  return process.env.API_INTERNAL_URL || process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    cache: "no-store",
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  })

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`)
  }

  return response.json() as Promise<T>
}

export async function getCourts(pageSize = 3, page = 1) {
  return requestJson<PagedResponse<Court>>(`/api/courts/?page_size=${pageSize}&page=${page}`)
}

export async function getCoaches(pageSize = 3, page = 1) {
  return requestJson<PagedResponse<Coach>>(`/api/coaches/?page_size=${pageSize}&page=${page}`)
}

export async function getTournaments(pageSize = 3, page = 1) {
  return requestJson<PagedResponse<Tournament>>(`/api/tournaments/?page_size=${pageSize}&page=${page}`)
}

export async function getCourt(id: string) {
  return requestJson<Court>(`/api/courts/${id}/`)
}

export async function getCoach(id: string) {
  return requestJson<Coach>(`/api/coaches/${id}/`)
}

export async function getTournament(id: string) {
  return requestJson<Tournament>(`/api/tournaments/${id}/`)
}

export async function searchPadel(query: string, filters: SearchFilters = {}, page = 1, pageSize = 8) {
  return requestJson<SearchResponse>("/api/search/", {
    method: "POST",
    body: JSON.stringify({ query, filters, page, page_size: pageSize }),
  })
}

export async function loginAdmin(username: string, password: string) {
  return requestJson<{ detail: string }>("/api/auth/login/", {
    method: "POST",
    credentials: "include",
    body: JSON.stringify({ username, password }),
  })
}
