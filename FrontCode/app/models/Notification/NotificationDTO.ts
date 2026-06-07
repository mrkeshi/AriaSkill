export type NotificationType =
  | 'login_failed'
  | 'comment_created'
  | 'like_received'
  | 'broadcast'

export interface NotificationDTO {
  id: number
  type: NotificationType
  title: string
  message: string
  related_project_id: number | null
  related_project_title: string | null
  related_project_slug: string | null
  related_user_id: number | null
  related_user_username: string | null
  metadata: Record<string, any>
  is_read: boolean
  created_at: string
  updated_at: string
}

export interface NotificationListDTO {
  count: number
  next: string | null
  previous: string | null
  results: NotificationDTO[]
}

export interface NotificationUnreadCountDTO {
  unread_count: number
}

export interface NotificationMarkAllReadDTO {
  updated: number
}

export interface BroadcastPayloadDTO {
  title: string
  message: string
}

export interface BroadcastResponseDTO {
  detail: string
  count: number
}
