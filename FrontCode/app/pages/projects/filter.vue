<template>
  <div class="grid grid-cols-1 min-h-screen lg:grid-cols-3 gap-8 py-8 lg:py-24">

    <div class="space-y-5">
      <ProjectFiltersBoxResult
        :filters="filters"
        :resetSearch="resetSearch"
        :resetAll="resetAll"
        :toggleTechnology="toggleTechnology"
        :toggleYears="toggleYears"
        :toggleCategory="toggleCategory"
      />

      <ProjectFiltersTechnology
        :filters="filters"
        :toggleTechnology="toggleTechnology"
      />

      <ProjectFiltersYears
        :filters="filters"
        :toggleYears="toggleYears"
      />

      <ProjectFiltersSearch
        :filters="filters"
        :apply-filter="applyFilter"
      />

      <ProjectFiltersCategory
        :filters="filters"
        :toggle-category="toggleCategory"
      />

      <div class="text-left">
        <ui-button @click="handleApplyFilter" w-full>فیلتر کردن نتایج</ui-button>
      </div>
    </div>


    <div class="lg:col-span-2">
      <div class="flex flex-col space-y-0">
        <ProjectFiltersSort :filters="filters" @sort-changed="handleSortChange" />

        <SkeletonSimple v-if="pending" :repeat="6" class="h-32 mb-3" />

        <div v-else-if="projects.length === 0" class="py-24 flex flex-col items-center gap-4 text-gray-400">
          <Icon name="mdi:folder-search-outline" size="56" class="opacity-40" />
          <p class="text-lg">پروژه‌ای با این فیلترها یافت نشد</p>
          <button @click="resetAll" class="text-classic-gold underline text-sm">پاک کردن فیلترها</button>
        </div>

        <ProjectContainer v-else lg-grid="2" min :projects="projects" />

        <UiPagination :totalPages="totalPages" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useProjectFilters } from '~/composable/useProjectFilters'
import { getPublicProjectsService } from '~/services/projects/project.Service'
import { generateSeoMeta } from '~/utilities/seo'

const { filters, applyFilter, resetSearch, resetAll, toggleTechnology, toggleYears, toggleCategory } = useProjectFilters()

const route = useRoute()
const currentPage = computed(() => Number(route.query.page) || 1)

const queryKey = computed(() => JSON.stringify(route.query))

const { data, pending, refresh } = await useAsyncData(
  'public-projects-filtered',
  () => {
    const q = route.query
    const techQuery = q.technology as string | undefined
    const yearQuery = q.year as string | undefined
    const catQuery = q.category as string | undefined

    return getPublicProjectsService(currentPage.value, 6, {
      q: (q.q as string) || undefined,
      technology: techQuery ? techQuery.split(',').filter(Boolean) : [],
      years: yearQuery ? yearQuery.split(',').map(Number).filter(Boolean) : [],
      category: catQuery ? (catQuery.split(',').filter(Boolean) as any) : [],
      sort: (q.sort as any) || 'new',
    })
  },
  { watch: [queryKey] }
)

const projects = computed(() => data.value?.data?.results ?? [])
const totalPages = computed(() => Math.ceil((data.value?.data?.count ?? 0) / 6))

const handleApplyFilter = () => {
  applyFilter()
  nextTick(() => refresh())
}

const handleSortChange = () => {
  applyFilter()
  nextTick(() => refresh())
}

const seo = generateSeoMeta({
  title: `فیلتر کردن پروژه‌ها`,
  description: 'جستجو و فیلتر پروژه‌ها بر اساس تکنولوژی، سال و دسته‌بندی',
  image: '',
  url: '',
  keywords: ['فیلتر پروژه', 'جستجو پروژه'],
  author: 'علیرضا کشاورز',
  type: 'website',
})
useHead(seo)
</script>