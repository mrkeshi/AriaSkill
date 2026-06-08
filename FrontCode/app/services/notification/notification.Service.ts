import type { ApiResponse } from '~/models/ApiResponseDTO'
import type { DashboardStatsDTO } from '~/models/Dashboard/dashboardTypes'
import type {
  BroadcastPayloadDTO,
  BroadcastResponseDTO,
  NotificationDTO,
  NotificationListDTO,
  NotificationMarkAllReadDTO,
  NotificationUnreadCountDTO,
  NotificationType,
} from '~/models/Notification/NotificationDTO'
import { FetchX } from '~/utilities/fetchX'

export const getRecentNotificationsService = (): Promise<ApiResponse<NotificationDTO[]>> =>
  FetchX('notifications/recent/', { method: 'get' })

export const getNotificationsService = (
  page = 1,
  type?: NotificationType,
  is_read?: boolean,
): Promise<ApiResponse<NotificationListDTO>> => {
  const query: Record<string, any> = { page }
  if (type)                  query.type    = type
  if (is_read !== undefined) query.is_read = is_read
  return FetchX('notifications/', { method: 'get', query })
}

export const getUnreadNotificationCountService = (): Promise<ApiResponse<NotificationUnreadCountDTO>> =>
  FetchX('notifications/unread-count/', { method: 'get' })

export const markNotificationReadService = (
  id: number,
  is_read = true,
): Promise<ApiResponse<NotificationDTO>> =>
  FetchX(`notifications/${id}/mark-read/`, { method: 'patch', body: { is_read } })

export const markAllNotificationsReadService = (): Promise<ApiResponse<NotificationMarkAllReadDTO>> =>
  FetchX('notifications/mark-all-read/', { method: 'patch' })

export const deleteNotificationService = (id: number): Promise<ApiResponse<null>> =>
  FetchX(`notifications/${id}/`, { method: 'delete' })

export const sendBroadcastService = (
  payload: BroadcastPayloadDTO,
): Promise<ApiResponse<BroadcastResponseDTO>> =>
  FetchX('notifications/admin/broadcast/', { method: 'post', body: payload })

export interface BroadcastLogDTO {
  id:               number
  title:            string
  message:          string
  sent_by_id:       number | null
  sent_by_username: string
  sent_to_count:    number
  sent_at:          string
}

export interface BroadcastLogListDTO {
  count:    number
  next:     string | null
  previous: string | null
  results:  BroadcastLogDTO[]
}

export const getBroadcastLogService = (
  page = 1,
): Promise<ApiResponse<BroadcastLogListDTO>> =>
  FetchX('notifications/admin/broadcast-log/', { method: 'get', query: { page } })

export const clearBroadcastLogService = (): Promise<ApiResponse<{ detail: string; deleted: number }>> =>
  FetchX('notifications/admin/broadcast-log/', { method: 'delete' })

export const getDashboardStatsService = (): Promise<ApiResponse<DashboardStatsDTO>> =>
  FetchX('project/dashboard/stats/', { method: 'get' })
