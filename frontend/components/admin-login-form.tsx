"use client"

import { useState } from "react"

import { loginAdmin } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function AdminLoginForm() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setLoading(true)
    setMessage(null)
    try {
      await loginAdmin(username, password)
      setMessage("Login successful. Open the Django admin in the backend service.")
    } catch {
      setMessage("Login failed. Check the admin credentials.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-[28px] border border-slate-200 bg-white p-6 shadow-soft">
      <div className="space-y-2">
        <label className="text-sm font-medium text-slate-700">Username</label>
        <Input value={username} onChange={(event) => setUsername(event.target.value)} placeholder="admin" autoComplete="username" />
      </div>
      <div className="space-y-2">
        <label className="text-sm font-medium text-slate-700">Password</label>
        <Input value={password} onChange={(event) => setPassword(event.target.value)} type="password" placeholder="••••••••" autoComplete="current-password" />
      </div>
      <Button type="submit" disabled={loading} className="w-full">
        {loading ? "Signing in..." : "Sign in"}
      </Button>
      {message ? <p className="text-sm text-slate-600">{message}</p> : null}
    </form>
  )
}
