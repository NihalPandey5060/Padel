import { AdminLoginForm } from "@/components/admin-login-form"
import { Badge } from "@/components/ui/badge"

export default function AdminPage() {
  return (
    <div className="mx-auto w-full max-w-2xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="space-y-4">
        <Badge>Admin access</Badge>
        <h1 className="font-display text-4xl font-semibold tracking-tight">Admin login</h1>
        <p className="max-w-2xl text-slate-600">Authenticate against the backend, then open the Django admin to manage courts, coaches, tournaments, and search logs.</p>
      </div>
      <div className="mt-8">
        <AdminLoginForm />
      </div>
      <p className="mt-4 text-sm text-slate-600">Backend admin: <a className="font-medium text-emerald-700 underline" href="http://localhost:8000/admin/" target="_blank" rel="noreferrer">http://localhost:8000/admin/</a></p>
    </div>
  )
}
