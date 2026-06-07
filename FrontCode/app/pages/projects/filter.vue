<template>
  <div class="grid grid-cols-1 min-h-screen lg:grid-cols-3 gap-8 py-8 lg:py-24">

    <!-- ستون فیلترها -->
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

    <!-- ستون نتایج -->
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

// ساخت کلید واچ از همه query params
const queryKey = computed(() => JSON.stringify(route.query))

const { data, pending, refresh } = await useAsyncData(
  'public-projects-filtered',
  () =>
    getPublicProjectsService(currentPage.value, 6, {
      q: filters.q || undefined,
      technology: filters.technology as string[],
      years: filters.years as number[],
      category: filters.category as any,
      sort: filters.sort,
    }),
  { watch: [queryKey] }
)

const projects = computed(() => data.value?.data?.results ?? [])
const totalPages = computed(() => Math.ceil((data.value?.data?.count ?? 0) / 6))

// اعمال فیلتر و رفرش
const handleApplyFilter = () => {
  applyFilter()
  nextTick(() => refresh())
}

// هنگام تغییر مرتب‌سازی
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