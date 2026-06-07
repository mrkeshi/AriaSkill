export interface SendCommentDTO {
  project: number
  parent: number | null
  message: string
}

export interface CommentDTO {
  id: number
  project: number
  user: number
  user_name: string
  user_avatar: string
  message: string
  status: 'active' | 'inactive'
  parent: number | null
  replies: CommentDTO[]
  created_at: string
  updated_at: string
}

export interface CommentManagementDTO extends CommentDTO {
  project_title: string
  project_slug: string
}

export interface CommentListDTO {
  count: number
  next: string | null
  previous: string | null
  results: CommentManagementDTO[]
}

export interface ProjectCommentListDTO {
  count: number
  next: string | null
  previous: string | null
  results: CommentDTO[]
}
