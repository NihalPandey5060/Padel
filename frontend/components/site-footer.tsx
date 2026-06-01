export function SiteFooter() {
  return (
    <footer className="border-t border-slate-200/80 bg-white/40">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-2 px-4 py-8 text-sm text-slate-600 sm:px-6 lg:px-8">
        <p>Designed for a local Docker MVP demo.</p>
        <p>Gemini filter extraction and JWT auth run only in the backend service.</p>
      </div>
    </footer>
  )
}
