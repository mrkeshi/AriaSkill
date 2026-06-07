export  interface SkillSDTO{
    results:skillItem[]
    count:number
    next:string
    previous:string
}
export interface CreateSkillDTO{
 name: string,
 icon: string
}

export interface skillItem{
 id: number,
 name: string,
 slug: string,
 icon: string
}

export type SkillDTO = skillItem
