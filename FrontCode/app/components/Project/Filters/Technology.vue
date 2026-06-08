<template>
  <UiAccordingCard title="تکنولوژی">
    <div v-if="pending" class="flex flex-wrap gap-2">
      <div
        v-for="i in 6"
        :key="i"
        class="h-9 w-20 rounded-md bg-white/5 animate-pulse"
      />
    </div>

    <div v-else-if="technologies.length" class="flex flex-wrap gap-2">
      <a
        v-for="tech in technologies"
        :key="tech.id"
        @click="toggleTechnology(tech.slug)"
        class="backdrop-blur-md shadow-xl p-2 transition cursor-pointer border rounded-md flex items-center gap-1.5"
        :class="
          filters.technology.includes(tech.slug)
            ? 'bg-classic-gold/20 border-classic-gold'
            : 'bg-carb-gray/40 border-white/10 hover:bg-carb-gray'
        "
      >
        <img
          v-if="tech.icon"
          :src="tech.icon"
          class="h-5 w-5 object-contain"
          :alt="tech.name"
        />
        <Icon v-else name="mdi:code-tags" class="h-5 w-5 text-gray-400" />
        
        <span
          class="text-sm"
          :class="
            filters.technology.includes(tech.slug)
              ? 'text-classic-gold'
              : 'text-white'
          "
        >
          {{ tech.name }}
        </span>
      </a>
    </div>

    <p v-else class="text-gray-400 text-sm">تکنولوژی‌ای یافت نشد</p>
  </UiAccordingCard>
</template>

<script lang="ts" setup>
import { getSkillsService } from '~/services/skills/skills.Service'
import type { skillItem } from '~/models/Skill/SkillDTO'

/**
 * Define component props received from the parent component.
 * - filters: Current active search query and selected technology slugs.
 * - toggleTechnology: Function callback to handle selection/deselection of a technology.
 */
const { filters, toggleTechnology } = defineProps<{
  filters: { q: string; technology: string[] }
  toggleTechnology: (slug: string) => void
}>()

// Component state reactive variables
const technologies = ref<skillItem[]>([])
const pending = ref(true)

/**
 * Fetches all skills/technologies from the API.
 * Handles pagination by dynamically sending parallel requests for subsequent pages.
 */
const loadAllSkills = async () => {
  pending.value = true
  try {
    // Fetch the first page to determine total items and page size
    const firstPage = await getSkillsService(1)
    const total = firstPage?.data?.count ?? 0
    const results = firstPage?.data?.results ?? []

    // If all items fit within the first page, assign directly
    if (total <= results.length) {
      technologies.value = results
    } else {
      // Calculate total pages based on first page items count (capped at max 10 pages)
      const pageSize = results.length || 10
      const totalPages = Math.ceil(total / pageSize)
      const all = [...results]
      const promises = []

      // Prepare parallel requests for pages 2 to N
      for (let p = 2; p <= Math.min(totalPages, 10); p++) {
        promises.push(getSkillsService(p))
      }
      
      // Resolve all page requests concurrently
      const pages = await Promise.all(promises)
      
      // Merge results from all resolved pages into a single array
      for (const page of pages) {
        all.push(...(page?.data?.results ?? []))
      }
      technologies.value = all
    }
  } catch (e) {
    console.error('خطا در بارگذاری تکنولوژی‌ها', e)
  } finally {
    // Hide loading skeleton regardless of outcome
    pending.value = false
  }
}

// Automatically trigger data fetching when the component mounts
onMounted(loadAllSkills)
</script>