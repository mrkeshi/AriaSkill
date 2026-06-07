/**
 * useAdminSearch
 *
 * Encapsulates the search/filter pattern common to all admin list pages:
 *   - searchInput: the v-model bound to the <input>
 *   - searchQuery: the committed query value read from the URL
 *   - submitSearch(): navigate to page 1 with search param set
 *   - clearSearch(): clear the param and navigate to page 1
 *
 * Usage:
 *   const { searchInput, searchQuery, submitSearch, clearSearch } = useAdminSearch()
 */
export const useAdminSearch = () => {
  const route  = useRoute()
  const router = useRouter()

  const searchQuery = computed(() => String(route.query.search || '').trim())
  const searchInput = ref(searchQuery.value)

  // Keep the input in sync when the URL changes (e.g. browser back/forward)
  watch(searchQuery, (val) => { searchInput.value = val })

  const submitSearch = () => {
    router.push({
      query: {
        ...route.query,
        page:   undefined,
        search: searchInput.value.trim() || undefined,
      },
    })
  }

  const clearSearch = () => {
    searchInput.value = ''
    router.push({
      query: {
        ...route.query,
        page:   undefined,
        search: undefined,
      },
    })
  }

  return { searchInput, searchQuery, submitSearch, clearSearch }
}
