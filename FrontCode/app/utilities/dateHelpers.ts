const LATIN_TO_PERSIAN: Record<string, string> = {
  '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
  '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹',
}

export const toPersianNumerals = (value: string | number | null | undefined): string => {
  if (value === null || value === undefined) return ''
  return String(value).replace(/[0-9]/g, (d) => LATIN_TO_PERSIAN[d] ?? d)
}

const PERSIAN_MONTHS: readonly string[] = [
  'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
  'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند',
]

const persianFormatter = new Intl.DateTimeFormat('fa-IR', {
  calendar: 'persian',
  numberingSystem: 'latn',
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
})

export const toJalali = (value?: string | Date | null): string => {
  if (!value) return '-'
  const date = value instanceof Date ? value : new Date(value)
  if (isNaN(date.getTime())) return '-'
  return toPersianNumerals(persianFormatter.format(date))
}

export const toJalaliLong = (value?: string | Date | null): string => {
  if (!value) return '-'
  const date = value instanceof Date ? value : new Date(value)
  if (isNaN(date.getTime())) return '-'

  const parts = new Intl.DateTimeFormat('fa-IR', {
    calendar: 'persian',
    numberingSystem: 'latn',
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
  }).formatToParts(date)

  const get = (type: string) => parts.find((p) => p.type === type)?.value ?? ''

  const day = get('day')
  const monthIndex = parseInt(get('month'), 10) - 1
  const year = get('year')
  const monthName = PERSIAN_MONTHS[monthIndex] ?? ''

  return `${toPersianNumerals(day)} ${monthName} ${toPersianNumerals(year)}`
}

export const toJalaliWithTime = (value?: string | Date | null): string => {
  if (!value) return '-'
  const date = value instanceof Date ? value : new Date(value)
  if (isNaN(date.getTime())) return '-'

  const parts = new Intl.DateTimeFormat('fa-IR', {
    calendar: 'persian',
    numberingSystem: 'latn',
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'Asia/Tehran',
  }).formatToParts(date)

  const get = (type: string) => parts.find((p) => p.type === type)?.value ?? ''

  const day = get('day')
  const monthIndex = parseInt(get('month'), 10) - 1
  const year = get('year')
  const hour = get('hour')
  const minute = get('minute')
  const monthName = PERSIAN_MONTHS[monthIndex] ?? ''

  return `${toPersianNumerals(day)} ${monthName} ${toPersianNumerals(year)} — ${toPersianNumerals(hour)}:${toPersianNumerals(minute)}`
}

export const getIranGreeting = (): string => {
  const iranTimeStr = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Asia/Tehran',
    hour: 'numeric',
    hour12: false,
  }).format(new Date())

  const hour = parseInt(iranTimeStr, 10)

  if (hour < 12) return 'صبح بخیر،'
  if (hour < 14) return 'ظهر بخیر،'
  if (hour < 21) return 'عصر بخیر،'
  return 'شب بخیر،'
}
