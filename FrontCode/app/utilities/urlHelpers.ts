import { baseURL } from './ApiConfig'

const hasProtocol = (url: string) => /^https?:\/\//i.test(url)

export const resolveMediaUrl = (url?: string | null) => {
  if (!url) return ''
  if (hasProtocol(url) || url.startsWith('blob:') || url.startsWith('data:')) return url

  const apiRoot = baseURL.replace(/\/api\/?$/, '/')
  return new URL(url, apiRoot).href
}

export const normalizeExternalUrl = (url?: string | null) => {
  const value = (url ?? '').trim()
  if (!value) return ''

  return hasProtocol(value) ? value : `https://${value}`
}

export const normalizeSocialLinks = <T extends Record<string, unknown>>(data: T) => ({
  ...data,
  instagram_link: normalizeExternalUrl(data.instagram_link as string | null | undefined),
  telegram_link: normalizeExternalUrl(data.telegram_link as string | null | undefined),
  discord_link: normalizeExternalUrl(data.discord_link as string | null | undefined),
  linkedin_link: normalizeExternalUrl(data.linkedin_link as string | null | undefined),
})
