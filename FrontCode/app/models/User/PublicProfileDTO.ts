// This file defines the types for the public user profile data transfer objects (DTOs) in a TypeScript project.

import type { SkillDTO } from '../Skill/SkillDTO'

export interface PublicProjectMiniDTO {
  id: number
  title: string
  slug: string
  image: string | null
  project_type: string
  project_type_display: string
  likes_count: number
  download_count: number
  view_count: number
  created_at: string
  skills: SkillDTO[]
}

export interface PublicUserProfileDTO {
  username: string
  full_name: string
  first_name: string
  last_name: string
  avatar: string | null
  job_title: string | null
  about_me: string | null
  instagram_link: string | null
  telegram_link: string | null
  discord_link: string | null
  linkedin_link: string | null
  date_joined: string
  projects: PublicProjectMiniDTO[]
  total_likes: number
  projects_count: number
}
