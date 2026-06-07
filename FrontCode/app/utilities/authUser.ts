import type { UserDTO } from '~/models/User/UserDTO'
import { resolveMediaUrl } from './urlHelpers'

export type AuthUserResponse = Partial<UserDTO> & {
  avatr?: string | null
  isAdmin?: boolean
  is_admin?: boolean
}

export const createEmptyUser = (): UserDTO => ({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  avatar: '',
  is_staff: false,
  is_superuser: false,
})

const asBoolean = (value: unknown) => value === true || value === 'true' || value === '1' || value === 1

export const normalizeAuthUser = (data: AuthUserResponse = {}): UserDTO => ({
  username: data.username ?? '',
  email: data.email ?? '',
  first_name: data.first_name ?? '',
  last_name: data.last_name ?? '',
  avatar: resolveMediaUrl(data.avatar ?? data.avatr),
  is_staff: asBoolean(data.is_staff ?? data.isAdmin ?? data.is_admin),
  is_superuser: asBoolean(data.is_superuser),
})
