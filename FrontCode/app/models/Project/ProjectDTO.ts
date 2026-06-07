import type { SkillDTO } from "../Skill/SkillDTO"
import type { UserSummaryDTO } from "../User/UserDTO"

export interface ProjectDTO{
    id:number
    title:string
    slug:string
    image:string | null
    file:string | null
    description:string
    created_at:string
    updated_at:string
    project_type:string
    project_type_display:string
    download_count:number
    view_count:number
    likes_count:number
    user_has_liked:boolean
    comments_count:number
    status:string
    user:UserSummaryDTO
    skills:SkillDTO[]
}
export interface ProjectListDTO{
    count:number
    next:string | null
    previous:string | null
    results:ProjectDTO[]
}

export interface CreateProjectDTO{
    title:string
    description:string
    image:File | null
    file?:File | null
    project_type:string
    skill_ids:number[]
}
