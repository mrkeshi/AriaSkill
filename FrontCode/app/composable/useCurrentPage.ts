/**
 * useCurrentPage
 *
 * Encapsulates the URL query-based current page pattern used across all
 * list pages. Replaces the repetitive one-liner:
 *   const currentPage = computed(() => Number(route.query.page) || 1)
 *
 * Also provides goToPage() for programmatic navigation (e.g. on filter reset).
 *
 * Usage:
 *   const { currentPage, goToPage } = useCurrentPage()
 */
export const useCurrentPage = () => {
  const route  = useRoute()
  const router = useRouter()

  const currentPage = computed(() => Number(route.query.page) || 1)

  const goToPage = (page: number) => {
    router.push({
      query: { ...route.query, page: page > 1 ? page : undefined },
    })
  }

  return { currentPage, goToPage }
}
