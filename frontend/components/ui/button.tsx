import * as React from "react"

import { cn } from "@/lib/utils"

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "secondary" | "ghost"
  size?: "default" | "sm"
}

export function Button({ className, variant = "default", size = "default", ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-full border text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 disabled:pointer-events-none disabled:opacity-50",
        variant === "default" && "border-transparent bg-emerald-600 text-white shadow-sm hover:bg-emerald-700",
        variant === "secondary" && "border-slate-200 bg-white text-slate-900 hover:bg-slate-50",
        variant === "ghost" && "border-transparent bg-transparent text-slate-700 hover:bg-slate-100",
        size === "default" && "h-11 px-5",
        size === "sm" && "h-9 px-4 text-xs",
        className,
      )}
      {...props}
    />
  )
}
