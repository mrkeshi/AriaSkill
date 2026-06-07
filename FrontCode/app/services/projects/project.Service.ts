import type { ApiResponse } from '~/models/ApiResponseDTO'
import type { CommentDTO, CommentListDTO, CommentManagementDTO, ProjectCommentListDTO, SendCommentDTO } from '~/models/Comment/SendCommentDTO'
import type { ProjectDTO, ProjectListDTO } from '~/models/Project/ProjectDTO'
import type { FilterProjectDTO } from '~/models/Project/FilterProjectDTO'
import { FetchX } from '~/utilities/fetchX'

export const getMyProjectsService = (page = 1): Promise<ApiResponse<ProjectListDTO>> => {
  return FetchX('project/', {
    method: 'get',
    query: { page },
  })
}

export const getPublicProjectsService = (
  page = 1,
  pageSize = 6,
  filters?: Partial<FilterProjectDTO>
): Promise<ApiResponse<ProjectListDTO>> => {
  const query: Record<string, any> = { page, page_size: pageSize }

  if (filters?.q) query.q = filters.q
  if (filters?.sort) query.sort = filters.sort
  if (filters?.technology?.length) query.technology = filters.technology
  if (filters?.years?.length) query.year = filters.years
  if (filters?.category?.length) query.category = filters.category

  return FetchX('project/projects/public/', {
    method: 'get',
    query,
  })
}

export const getProjectYearsService = (): Promise<ApiResponse<{ years: number[] }>> => {
  return FetchX('project/projects/years/', {
    method: 'get',
  })
}

export const createProjectService = (data: FormData): Promise<ApiResponse<ProjectDTO>> => {
  return FetchX('project/', {
    method: 'post',
    body: data,
  })
}

export const retrieveProjectService = (slug: string): Promise<ApiResponse<ProjectDTO>> => {
  return FetchX(`project/${slug}/`, {
    method: 'get',
  })
}

export const likeProjectService = (slug: string): Promise<ApiResponse<{ likes_count: number; liked: boolean }>> => {
  return FetchX(`project/${slug}/like/`, {
    method: 'post',
  })
}

export const unlikeProjectService = (slug: string): Promise<ApiResponse<{ likes_count: number; liked: boolean }>> => {
  return FetchX(`project/${slug}/unlike/`, {
    method: 'post',
  })
}

export const downloadProjectService = (slug: string): Promise<ApiResponse<{ download_count: number }>> => {
  return FetchX(`project/${slug}/download/`, {
    method: 'post',
  })
}

export const getProjectCommentsService = (projectId: number, page = 1): Promise<ApiResponse<ProjectCommentListDTO | CommentDTO[]>> => {
  return FetchX(`project/${projectId}/comments/`, {
    method: 'get',
    query: { page },
  })
}

export const sendProjectCommentService = (projectId: number, data: Pick<SendCommentDTO, 'message' | 'parent'>): Promise<ApiResponse<CommentDTO>> => {
  return FetchX(`project/${projectId}/comments/`, {
    method: 'post',
    body: {
      project: projectId,
      ...data,
    },
  })
}

export const deleteCommentService = (commentId: number): Promise<ApiResponse<null>> => {
  return FetchX(`project/comments/${commentId}/`, {
    method: 'delete',
  })
}

export const getMyProjectCommentsService = (page = 1): Promise<ApiResponse<CommentListDTO>> => {
  return FetchX('project/comments/my-projects/', {
    method: 'get',
    query: { page },
  })
}

export const updateMyProjectCommentStatusService = (
  id: number,
  status: 'pending' | 'approved' | 'rejected',
): Promise<ApiResponse<CommentManagementDTO>> => {
  return FetchX(`project/comments/my-projects/${id}/`, {
    method: 'patch',
    body: { status },
  })
}

export const deleteMyProjectCommentService = (id: number): Promise<ApiResponse<null>> => {
  return FetchX(`project/comments/my-projects/${id}/`, {
    method: 'delete',
  })
}

export const updateProjectService = (slug: string, data: FormData): Promise<ApiResponse<ProjectDTO>> => {
  return FetchX(`project/${slug}/`, {
    method: 'patch',
    body: data,
  })
}

export const deleteProjectService = (slug: string): Promise<ApiResponse<null>> => {
  return FetchX(`project/${slug}/`, {
    method: 'delete',
  })
}

export const getAdminProjectsService = (page = 1, search = ''): Promise<ApiResponse<ProjectListDTO>> => {
  return FetchX('project/admin/projects/', {
    method: 'get',
    query: { page, search: search || undefined },
  })
}

export const deleteAdminProjectService = (slug: string): Promise<ApiResponse<null>> => {
  return FetchX(`project/admin/projects/${slug}/`, {
    method: 'delete',
  })
}

export const updateAdminProjectStatusService = (slug: string, is_active: boolean): Promise<ApiResponse<ProjectDTO>> => {
  return FetchX(`project/admin/projects/${slug}/status/`, {
    method: 'patch',
    body: { is_active },
  })
}

export const getAdminCommentsService = (
  page = 1,
  search = '',
  status?: 'active' | 'inactive',
): Promise<ApiResponse<CommentListDTO>> => {
  return FetchX('project/admin/comments/', {
    method: 'get',
    query: {
      page,
      search: search || undefined,
      status: status || undefined,
    },
  })
}

export const updateAdminCommentStatusService = (
  id: number,
  status: 'active' | 'inactive',
): Promise<ApiResponse<CommentManagementDTO>> => {
  return FetchX(`project/admin/comments/${id}/`, {
    method: 'patch',
    body: { status },
  })
}

export const deleteAdminCommentService = (id: number): Promise<ApiResponse<null>> => {
  return FetchX(`project/admin/comments/${id}/`, {
    method: 'delete',
  })
}