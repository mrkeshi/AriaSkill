<template>
  <ui-card-blury>
    <h2 class="text-xl font-semibold text-white mb-4">فیلتر اعمال شده</h2>
    <div class="flex flex-wrap w-full gap-3">

      <!-- جستجوی متنی -->
      <a
        v-if="filters.q"
        class="backdrop-blur-md transition relative hover:opacity-50 shadow-2xl p-2 bg-carb-gray/40 border border-white/10 rounded-md flex items-center gap-1.5"
      >
        <span class="text-white text-sm">
          <Icon
            @click="() => resetSearch()"
            name="mdi:close"
            size="12"
            class="text-white absolute hover:text-light-gold -left-0 top-1 cursor-pointer"
          />
          <span class="text-light-gold">جستجو:</span> {{ filters.q }}
        </span>
      </a>

      <!-- تکنولوژی‌های انتخاب‌شده -->
      <template v-if="selectedTechObjects.length">
        <a
          v-for="tech in selectedTechObjects"
          :key="tech.slug"
          class="backdrop-blur-md transition relative hover:opacity-50 shadow-2xl p-2 bg-carb-gray/40 border border-white/10 rounded-md flex items-center gap-1.5"
        >
          <Icon
            @click="() => toggleTechnology(tech.slug)"
            name="mdi:close"
            size="12"
            class="absolute left-0 top-1 text-white cursor-pointer"
          />
          <img v-if="tech.icon" :src="tech.icon" class="h-4 w-4 object-contain" />
          <span class="text-white text-sm">{{ tech.name }}</span>
        </a>
      </template>

      <!-- سال‌های انتخاب‌شده -->
      <template v-if="filters.years.length">
        <a
          v-for="year in filters.years"
          :key="year"
          class="backdrop-blur-md transition relative hover:opacity-50 shadow-2xl p-2 bg-carb-gray/40 border border-white/10 rounded-md flex items-center gap-1.5"
        >
          <Icon
            @click="() => toggleYears(year)"
            name="mdi:close"
            size="12"
            class="absolute left-0 top-1 text-white cursor-pointer"
          />
          <span class="text-white text-sm">
            <span class="text-classic-gold">سال:</span> {{ year }}
          </span>
        </a>
      </template>

      <!-- دسته‌بندی‌های انتخاب‌شده -->
      <template v-if="filters.category.length">
        <a
          v-for="cat in filters.category"
          :key="cat"
          class="backdrop-blur-md transition relative hover:opacity-50 shadow-2xl p-2 bg-carb-gray/40 border border-white/10 rounded-md flex items-center gap-1.5"
        >
          <Icon
            @click="() => toggleCategory(cat)"
            name="mdi:close"
            size="12"
            class="absolute left-0 top-1 text-white cursor-pointer"
          />
          <span class="text-white text-sm">
            <span class="text-classic-gold">نوع:</span> {{ cat }}
          </span>
        </a>
      </template>

      <!-- دکمه پاک کردن همه -->
      <a
        v-if="hasActiveFilters"
        @click="resetAll"
        class="backdrop-blur-md transition hover:opacity-70 shadow-2xl p-2 bg-red-900/20 border border-red-500/30 rounded-md flex items-center gap-1.5 cursor-pointer"
      >
        <Icon name="mdi:filter-remove" size="14" class="text-red-400" />
        <span class="text-red-400 text-sm">پاک کردن همه</span>
      </a>

      <p
        v-if="!hasActiveFilters"
        class="text-gray-500 text-sm w-full text-center py-1"
      >
        هیچ فیلتری اعمال نشده
      </p>
    </div>
  </ui-card-blury>
</template>

<script lang="ts" setup>
import type { ProjectCategory } from '~/models/Project/FilterProjectDTO'
import type { skillItem } from '~/models/Skill/SkillDTO'
import { getSkillsService } from '~/services/skills/skills.Service'

const {
  filters,
  resetSearch,
  toggleTechnology,
  toggleYears,
  toggleCategory,
  resetAll,
} = defineProps<{
  filters: {
    q: string
    technology: string[]
    years: number[]
    category: ProjectCategory[]
  }
  resetSearch: () => void
  resetAll: () => void
  toggleTechnology: (slug: string) => void
  toggleYears: (year: number) => void
  toggleCategory: (cat: ProjectCategory) => void
}>()

// کش تکنولوژی‌ها برای نمایش نام و آیکون
const allTechnologies = ref<skillItem[]>([])

onMounted(async () => {
  try {
    const firstPage = await getSkillsService(1)
    const total = firstPage?.data?.count ?? 0
    const results = firstPage?.data?.results ?? []
    if (total <= results.length) {
      allTechnologies.value = results
    } else {
      const all = [...results]
      const pageSize = results.length || 10
      const totalPages = Math.ceil(total / pageSize)
      const promises = []
      for (let p = 2; p <= Math.min(totalPages, 10); p++) {
        promises.push(getSkillsService(p))
      }
      const pages = await Promise.all(promises)
      for (const page of pages) all.push(...(page?.data?.results ?? []))
      allTechnologies.value = all
    }
  } catch (e) {
    console.error('خطا در بارگذاری تکنولوژی‌ها', e)
  }
})

const selectedTechObjects = computed(() =>
  filters.technology
    .map(slug => allTechnologies.value.find(t => t.slug === slug))
    .filter((t): t is skillItem => Boolean(t))
)

const hasActiveFilters = computed(
  () =>
    !!filters.q ||
    filters.technology.length > 0 ||
    filters.years.length > 0 ||
    filters.category.length > 0
)
</script>