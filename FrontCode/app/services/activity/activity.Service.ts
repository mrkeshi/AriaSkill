import type { ApiResponse } from '~/models/ApiResponseDTO'
import type {
  ActivityDTO,
  ActivityListDTO,
  ActivityMarkAllSeenDTO,
  ActivityType,
  ActivityUnseenCountDTO,
} from '~/models/Activity/ActivityDTO'
import { FetchX } from '~/utilities/fetchX'

export const getRecentActivitiesService = (): Promise<ApiResponse<ActivityDTO[]>> => {
  return FetchX('activities/recent/', { method: 'get' })
}

export const getActivitiesService = (
  page = 1,
  type?: ActivityType,
  is_seen?: boolean,
): Promise<ApiResponse<ActivityListDTO>> => {
  const query: Record<string, any> = { page }
  if (type) query.type = type
  if (is_seen !== undefined) query.is_seen = is_seen
  return FetchX('activities/', { method: 'get', query })
}

export const markActivitySeenService = (
  id: number,
  is_seen = true,
): Promise<ApiResponse<ActivityDTO>> => {
  return FetchX(`activities/${id}/mark-seen/`, {
    method: 'patch',
    body: { is_seen },
  })
}

export const deleteActivityService = (id: number): Promise<ApiResponse<null>> => {
  return FetchX(`activities/${id}/`, { method: 'delete' })
}

export const getUnseenActivityCountService = (): Promise<ApiResponse<ActivityUnseenCountDTO>> => {
  return FetchX('activities/unseen-count/', { method: 'get' })
}

export const markAllActivitiesSeenService = (): Promise<ApiResponse<ActivityMarkAllSeenDTO>> => {
  return FetchX('activities/mark-all-seen/', { method: 'patch' })
}
