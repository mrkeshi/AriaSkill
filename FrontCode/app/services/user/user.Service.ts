import type { ApiResponse } from "~/models/ApiResponseDTO";
import type { ActiveUserDTO, AuthUserDTO, ChangePasswordDTO, LoginDTO, RefTokenDTO } from "~/models/User/AuthDTO";
import type { RegisterDTO } from "~/models/User/AuthDTO";
import type { EditUserDTO } from "~/models/User/EditUserDTO";
import type { AdminUserDTO, AdminUserListDTO, AdminUserPasswordDTO, UserDTO } from "~/models/User/UserDTO";
import { FetchX } from "~/utilities/fetchX";


export const registerUserService=(data:RegisterDTO):Promise<ApiResponse<null>> =>{

    return FetchX("account/register/",{
        method:'post',
        body:data
    })
}

export const LoginUserService=(data:LoginDTO):Promise<ApiResponse<AuthUserDTO>> =>{

    return FetchX("account/login/",{
        method:'post',
        body:data
    })
}

export const googleAuthService=(credential:string):Promise<ApiResponse<AuthUserDTO>> =>{
    return FetchX("account/google/",{
        method:'post',
        body:{credential}
    })
}

export const refreshTokenService=(ref:string|null):Promise<ApiResponse<RefTokenDTO>> => {
    return FetchX("account/token/refresh/",{
        method:'post',
        body:{refresh:ref}
    })
}

export const sendResetLinkPassService=(email:string):Promise<ApiResponse<{message:string}>>=>{
     return FetchX("account/password_reset/request/",{
        method:'POST',
        body:{email}
    })
}
export const changePasswordService=(data:ChangePasswordDTO):Promise<ApiResponse<null>>=>{

     return FetchX("account/password_reset/confirm/",{
        method:'POST',
        body:data
    })
}

export const activeUserService=(data:ActiveUserDTO):Promise<ApiResponse<null>>=>{

     return FetchX("account/register/activate/",{
        method:'POST',
        body:data
    })
}
export const fetchUserService=():Promise<ApiResponse<UserDTO>>=>{
     return FetchX("account/profile/",{
        method:'GET',
    })
}
export const getEditUserService=():Promise<ApiResponse<EditUserDTO>>=>{
     return FetchX("account/profile/",{
        method:'GET',
    })
}

export const editUserService=(data:FormData):Promise<ApiResponse<EditUserDTO>>=>{
     return FetchX("account/profile/edit/",{
        method:'PATCH',
        body:data
    })
}

export const getAdminUsersService = (page: number = 1, search = ''): Promise<ApiResponse<AdminUserListDTO>> => {
    return FetchX("account/admin/users/", {
        method: 'GET',
        query: { page, search: search || undefined }
    })
}

export const deleteAdminUserService = (id: number): Promise<ApiResponse<null>> => {
    return FetchX(`account/admin/users/${id}/`, {
        method: 'DELETE'
    })
}

export const updateAdminUserStatusService = (id: number, is_active: boolean): Promise<ApiResponse<AdminUserDTO>> => {
    return FetchX(`account/admin/users/${id}/status/`, {
        method: 'PATCH',
        body: { is_active }
    })
}

export const changeAdminUserPasswordService = (id: number, data: AdminUserPasswordDTO): Promise<ApiResponse<{ message: string }>> => {
    return FetchX(`account/admin/users/${id}/password/`, {
        method: 'PATCH',
        body: data
    })
}
