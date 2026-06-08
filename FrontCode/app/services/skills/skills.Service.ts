// This file defines the services for handling skill-related operations in a TypeScript project.
import type { ApiResponse } from "~/models/ApiResponseDTO"
import type { CreateSkillDTO, skillItem, SkillSDTO } from "~/models/Skill/SkillDTO"
import { FetchX } from "~/utilities/fetchX"


export const createSkillService=(data:CreateSkillDTO):Promise<ApiResponse<any>> =>{
    return FetchX("project/skills/",{
        method:'post',
        body:data
    })
}
export const getSkillsService = (page: number = 1, search = ''): Promise<ApiResponse<SkillSDTO>> => {
  return FetchX("project/skills/", {
    method: 'get',
    query: { page, search: search || undefined }
  })
}
export const deleteSkillsService = (id:number): Promise<ApiResponse<any>> => {

  return FetchX(`project/skills/${id}/`, {
    method: 'delete',
   
  })
}
export const retriveSkillsService = (id: number): Promise<ApiResponse<skillItem>> => {
  return FetchX(`project/skills/${id}/`, {
    method: 'get',
  })
}

export const editSkillService = (data: FormData, id: number): Promise<ApiResponse<skillItem>> => {
  return FetchX(`project/skills/${id}/`, {
    method: 'patch',
    body: data,
  })
}
