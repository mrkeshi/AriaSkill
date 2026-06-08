import type { FilterProjectDTO, ProjectCategory, FilterSort } from "~/models/Project/FilterProjectDTO"
// Composable that manages project filters based on URL query parameters, allowing users to toggle filters for technology, years, and categories, and apply or reset filters while keeping the URL in sync with the current filter state

export const useProjectFilters = () => {
  const route = useRoute()
  const router = useRouter()

  const filters = reactive<FilterProjectDTO>({
    page: 1,
    category: [],
    years: [],
    q: '',
    sort: 'new',
    technology: []
  })

  const toggleItem = <T>(arr: T[], item: T) => {
    const index = arr.indexOf(item)
    if (index === -1) arr.push(item)
    else arr.splice(index, 1)
  }

  const toggleTechnology = (slug: string) => {
    toggleItem(filters.technology as string[], slug)
  }

  const toggleYears = (year: number) => {
    toggleItem(filters.years as number[], year)
  }

  const toggleCategory = (cat: ProjectCategory) => {
    toggleItem(filters.category as ProjectCategory[], cat)
  }

  const applyFilter = (): FilterProjectDTO => {
    const query: Record<string, any> = { ...route.query }

    if (filters.q) query.q = filters.q
    else delete query.q

    if ((filters.technology as string[]).length)
      query.technology = (filters.technology as string[]).join(',')
    else delete query.technology

    if ((filters.years as number[]).length)
      query.year = (filters.years as number[]).join(',')
    else delete query.year

    if ((filters.category as ProjectCategory[]).length)
      query.category = (filters.category as ProjectCategory[]).join(',')
    else delete query.category

    if (filters.sort && filters.sort !== 'new') query.sort = filters.sort
    else delete query.sort

    query.page = '1'

    router.replace({ query })

    return { ...filters }
  }

  const readFromQuery = () => {
    filters.q = (Array.isArray(route.query.q) ? route.query.q[0] : route.query.q) ?? ''

    const techQuery = route.query.technology
    filters.technology = techQuery
      ? (Array.isArray(techQuery) ? techQuery[0] : techQuery)?.split(',').filter(Boolean) ?? []
      : []

    const yearQuery = route.query.year
    const yearStr = Array.isArray(yearQuery) ? yearQuery[0] : yearQuery
    filters.years = yearStr
      ? yearStr.split(',').map(Number).filter(Boolean)
      : []

    const catQuery = route.query.category
    const catStr = Array.isArray(catQuery) ? catQuery[0] : catQuery
    filters.category = catStr
      ? (catStr.split(',').filter(Boolean) as ProjectCategory[])
      : []

    const sortQuery = route.query.sort
    filters.sort = ((Array.isArray(sortQuery) ? sortQuery[0] : sortQuery) as FilterSort) || 'new'
  }

  const resetSearch = () => {
    filters.q = ''
    applyFilter()
  }

  const resetAll = () => {
    filters.q = ''
    filters.technology = []
    filters.years = []
    filters.category = []
    filters.sort = 'new'
    router.replace({ query: {} })
  }

  onBeforeMount(readFromQuery)

  return {
    filters,
    applyFilter,
    resetSearch,
    resetAll,
    toggleTechnology,
    toggleYears,
    toggleCategory
  }
}