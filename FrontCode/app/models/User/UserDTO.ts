// This file defines the types for the User data transfer objects (DTOs) in a TypeScript project.
export interface UserDTO{
    username:string,
    email:string,
    first_name:string,
    last_name:string,
    avatar:null | string,
    is_staff:boolean,
    is_superuser:boolean,
}
export interface UserSummaryDTO{
    username:string
    id:number
    full_name:string,
    avatar:string
}

export interface AdminUserDTO {
    id:number
    username:string
    email:string
    first_name:string
    last_name:string
    avatar:null | string
    job_title:null | string
    is_active:boolean
    is_staff:boolean
    is_superuser:boolean
    date_joined:string
    last_login:string
}

export interface AdminUserListDTO {
    count:number
    next:string | null
    previous:string | null
    results:AdminUserDTO[]
}

export interface AdminUserPasswordDTO {
    password:string
    password_confirm:string
}
