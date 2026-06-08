// This file defines the types for the authentication-related data transfer objects (DTOs) in a TypeScript project.
// It includes interfaces for login, registration, password reset, and user activation processes, as well as the structure of the authenticated user data.
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
