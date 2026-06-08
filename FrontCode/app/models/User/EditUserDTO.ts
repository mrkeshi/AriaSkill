// This file defines the types for editing user information in a TypeScript project.
export interface EditUserDTO{
    avatar:null | string | File,
    avatr?:null | string,
    username:string,
    email:string,
    first_name:string,
    last_name:string,
    job_title:string,
    about_me:string,
    discord_link:string,
    telegram_link:string,
    instagram_link:string,
    linkedin_link:string,
}
