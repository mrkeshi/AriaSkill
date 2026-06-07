// ─── Project status helpers ────────────────────────────────────────────────

export type ProjectStatus = 'pending' | 'approved' | 'rejected' | string

/** Persian label for a project status value. */
export const projectStatusLabel = (status: ProjectStatus): string => {
  const labels: Record<string, string> = {
    pending:  'در انتظار بررسی',
    approved: 'فعال',
    rejected: 'غیرفعال',
  }
  return labels[status] ?? status
}

/** Tailwind badge classes for a project status value. */
export const projectStatusClass = (status: ProjectStatus): string => {
  const classes: Record<string, string> = {
    pending:  'bg-amber-500/10 text-amber-300 border-amber-500/30',
    approved: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30',
    rejected: 'bg-rose-500/10 text-rose-300 border-rose-500/30',
  }
  return classes[status] ?? 'bg-white/10 text-gray-300 border-white/20'
}

/** Tailwind dot color class for a project status value. */
export const projectStatusDotClass = (status: ProjectStatus): string => {
  const classes: Record<string, string> = {
    pending:  'bg-amber-400',
    approved: 'bg-emerald-400',
    rejected: 'bg-rose-400',
  }
  return classes[status] ?? 'bg-gray-400'
}
