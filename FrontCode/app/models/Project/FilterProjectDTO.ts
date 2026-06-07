
export type ProjectCategory =
  | "UI/UX Design"
  | "Frontend Development"
  | "Backend Development"
  | "Mobile Development"
  | "AI & Data"
  | "DevOps & Cloud"
  | "Game Development"
  | "Cyber Security"

export type FilterSort= "popular" | "new" | "old" | "downloads"
export type FilterProjectDTO = {
    page?:number
    category?: ProjectCategory | ProjectCategory[] 
    years?:number | number[]
    technology?: string[]
    q?:string | null,
    sort:FilterSort
}