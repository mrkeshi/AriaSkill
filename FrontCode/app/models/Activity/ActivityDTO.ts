// This file defines the data transfer objects (DTOs) for activities in the application. It includes the types of activities, the structure of an activity, and the structure of responses for listing activities, counting unseen activities, and marking all activities as seen.
export type ActivityType =
  | 'login_success'
  | 'login_failed'
  | 'project_published'
  | 'project_created'
  | 'project_updated'
  | 'project_deleted'
  | 'password_changed'
  | 'project_documentation_downloaded'
  | 'external_project_comment_created'
  | 'comment_created'

export interface ActivityDTO {
  id: number
  user_id: number
  type: ActivityType
  title: string
  description: string
  related_project_id: number | null
  related_project_title: string | null
  related_project_slug: string | null
  related_user_id: number | null
  related_user_username: string | null
  metadata: Record<string, any>
  is_seen: boolean
  created_at: string
  updated_at: string
}

export interface ActivityListDTO {
  count: number
  next: string | null
  previous: string | null
  results: ActivityDTO[]
}

export interface ActivityUnseenCountDTO {
  unseen_count: number
}

export interface ActivityMarkAllSeenDTO {
  updated: number
}
