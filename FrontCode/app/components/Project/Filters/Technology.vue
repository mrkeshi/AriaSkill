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

const { filters, toggleTechnology } = defineProps<{
  filters: { q: string; technology: string[] }
  toggleTechnology: (slug: string) => void
}>()

const technologies = ref<skillItem[]>([])
const pending = ref(true)

const loadAllSkills = async () => {
  pending.value = true
  try {
    // بارگذاری همه تکنولوژی‌ها (بدون صفحه‌بندی)
    const firstPage = await getSkillsService(1)
    const total = firstPage?.data?.count ?? 0
    const results = firstPage?.data?.results ?? []

    if (total <= results.length) {
      technologies.value = results
    } else {
      // اگر بیشتر از یک صفحه داشتیم همه رو بگیریم
      const pageSize = results.length || 10
      const totalPages = Math.ceil(total / pageSize)
      const all = [...results]
      const promises = []
      for (let p = 2; p <= Math.min(totalPages, 10); p++) {
        promises.push(getSkillsService(p))
      }
      const pages = await Promise.all(promises)
      for (const page of pages) {
        all.push(...(page?.data?.results ?? []))
      }
      technologies.value = all
    }
  } catch (e) {
    console.error('خطا در بارگذاری تکنولوژی‌ها', e)
  } finally {
    pending.value = false
  }
}

onMounted(loadAllSkills)
</script>