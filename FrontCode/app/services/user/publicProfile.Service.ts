// This file defines the service for fetching a user's public profile in a TypeScript project.
import type { ApiResponse } from '~/models/ApiResponseDTO'
import type { PublicUserProfileDTO } from '~/models/User/PublicProfileDTO'
import { FetchX } from '~/utilities/fetchX'

export const getPublicUserProfileService = (
  username: string,
): Promise<ApiResponse<PublicUserProfileDTO>> => {
  return FetchX(`account/users/${username}/`, { method: 'get' })
}
