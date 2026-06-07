import type { ApiResponse } from '~/models/ApiResponseDTO'
import type { PublicUserProfileDTO } from '~/models/User/PublicProfileDTO'
import { FetchX } from '~/utilities/fetchX'

export const getPublicUserProfileService = (
  username: string,
): Promise<ApiResponse<PublicUserProfileDTO>> => {
  return FetchX(`account/users/${username}/`, { method: 'get' })
}
