// This file defines the types for filtering projects in a TypeScript project.
// It includes the ProjectCategory type, which lists various categories of projects, and the FilterProjectDTO type, which specifies the structure of the data transfer object used for filtering projects based on various criteria such as category, years, technology, search query, and sorting options.
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