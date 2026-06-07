/**
 * Returns the first character of a name string, uppercased.
 * Used for avatar fallback initials throughout the dashboard.
 *
 * @example firstLetter('علیرضا کشاورز') // 'ع'
 * @example firstLetter(null)             // '?'
 */
export const firstLetter = (value?: string | null): string => {
  if (!value) return '?'
  return Array.from(value.trim())[0]?.toUpperCase() ?? '?'
}

/**
 * Returns the initial letter for a user object that may have
 * full_name, first_name, username, or email fields.
 * Priority: full_name → first_name → username → email → 'U'
 */
export const userInitialFrom = (user: {
  full_name?:  string | null
  first_name?: string | null
  username?:   string | null
  email?:      string | null
} | null | undefined): string => {
  const name =
    user?.full_name?.trim()  ||
    user?.first_name?.trim() ||
    user?.username?.trim()   ||
    user?.email?.trim()      ||
    'U'
  return Array.from(name)[0]?.toUpperCase() ?? 'U'
}

/**
 * Computes a page-relative row number for admin tables.
 * @param index   0-based index in the current page's array
 * @param page    current page number (1-based)
 * @param pageSize number of items per page
 */
export const rowNumber = (index: number, page: number, pageSize: number): number =>
  (page - 1) * pageSize + index + 1
