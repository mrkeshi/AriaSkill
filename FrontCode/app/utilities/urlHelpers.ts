import { baseURL } from './ApiConfig'

/**
 * Validates whether a given URL string starts with a standard HTTP or HTTPS protocol.
 */
const hasProtocol = (url: string) => /^https?:\/\//i.test(url)

/**
 * Resolves relative media assets or avatar paths into fully qualified absolute URLs.
 * Automatically bypasses conversion for external links, blobs, or base64 data URIs.
 */
export const resolveMediaUrl = (url?: string | null) => {
  if (!url) return ''
  if (hasProtocol(url) || url.startsWith('blob:') || url.startsWith('data:')) return url

  const apiRoot = baseURL.replace(/\/api\/?$/, '/')
  return new URL(url, apiRoot).href
}

/**
 * Enforces a fallback protocol secure prefix (https://) onto user-generated external domain strings.
 */
export const normalizeExternalUrl = (url?: string | null) => {
  const value = (url ?? '').trim()
  if (!value) return ''

  return hasProtocol(value) ? value : `https://${value}`
}

/**
 * Sanitizes and normalizes an unverified packet of profile social network links inside a single record wrapper.
 */
export const normalizeSocialLinks = <T extends Record<string, unknown>>(data: T) => ({
  ...data,
  instagram_link: normalizeExternalUrl(data.instagram_link as string | null | undefined),
  telegram_link: normalizeExternalUrl(data.telegram_link as string | null | undefined),
  discord_link: normalizeExternalUrl(data.discord_link as string | null | undefined),
  linkedin_link: normalizeExternalUrl(data.linkedin_link as string | null | undefined),
})