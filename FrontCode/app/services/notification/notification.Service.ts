import type { ApiResponse } from '~/models/ApiResponseDTO'
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

// ── Read ──────────────────────────────────────────────────────────────────

export const getRecentNotificationsService = (): Promise<ApiResponse<NotificationDTO[]>> =>
  FetchX('notifications/recent/', { method: 'get' })

export const getNotificationsService = (
  page = 1,
  type?: NotificationType,
  is_read?: boolean,
): Promise<ApiResponse<NotificationListDTO>> => {
  const query: Record<string, any> = { page }
  if (type)              query.type    = type
  if (is_read !== undefined) query.is_read = is_read
  return FetchX('notifications/', { method: 'get', query })
}

export const getUnreadNotificationCountService = (): Promise<ApiResponse<NotificationUnreadCountDTO>> =>
  FetchX('notifications/unread-count/', { method: 'get' })

// ── Write ─────────────────────────────────────────────────────────────────

export const markNotificationReadService = (
  id: number,
  is_read = true,
): Promise<ApiResponse<NotificationDTO>> =>
  FetchX(`notifications/${id}/mark-read/`, { method: 'patch', body: { is_read } })

export const markAllNotificationsReadService = (): Promise<ApiResponse<NotificationMarkAllReadDTO>> =>
  FetchX('notifications/mark-all-read/', { method: 'patch' })

export const deleteNotificationService = (id: number): Promise<ApiResponse<null>> =>
  FetchX(`notifications/${id}/`, { method: 'delete' })

// ── Admin ─────────────────────────────────────────────────────────────────

export const sendBroadcastService = (
  payload: BroadcastPayloadDTO,
): Promise<ApiResponse<BroadcastResponseDTO>> =>
  FetchX('notifications/admin/broadcast/', { method: 'post', body: payload })

// ── Dashboard stats ───────────────────────────────────────────────────────

export interface DashboardStatsDTO {
  total_projects: number
  total_downloads: number
  total_comments: number
  unread_notifications: number
}

export const getDashboardStatsService = (): Promise<ApiResponse<DashboardStatsDTO>> =>
  FetchX('project/dashboard/stats/', { method: 'get' })
