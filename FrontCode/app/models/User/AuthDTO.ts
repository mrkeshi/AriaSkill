import type { UserDTO } from "./UserDTO"

export interface LoginDTO{
    identifier:string,
    password:string
}
export interface ResetPassDTO{
    password:string,
    password_confirm:string
}

export interface AuthUserDTO{
    user:UserDTO,
    refresh:string,
    access:string
}
export interface RefTokenDTO{
  access: string
  refresh?: string
}
export interface RegisterDTO{
    username:string,
    first_name:string,
    last_name:string,
    email:string,
    password:string,
    password_confirm:string
}

export interface ChangePasswordDTO{
    uid:string,
    token:string,
    password:string,
    password_confirm:string
}
export interface ActiveUserDTO{
    uid:string,
    token:string
}
