<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between px-1">
      <label class="text-sm font-semibold text-gray-200 tracking-wide flex items-center gap-2">
        <Icon name="mdi:lightning-bolt" class="text-classic-gold text-base" />
        مهارت‌ها
      </label>
      <span 
        v-if="selectedSkills.length" 
        class="text-[11px] font-bold text-classic-gold bg-classic-gold/10 border border-classic-gold/20 px-2.5 py-1 rounded-full shadow-sm shadow-classic-gold/5"
      >
        {{ selectedSkills.length }} مورد انتخاب شده
      </span>
    </div>

    <div class="rounded-2xl border border-white/10 bg-white/[0.03] backdrop-blur-xl overflow-hidden shadow-2xl relative">
      
      <div class="relative border-b border-white/[0.08] group/search">
        <Icon 
          name="mdi:magnify" 
          class="absolute right-3.5 top-1/2 -translate-y-1/2 text-gray-400 text-xl pointer-events-none transition-colors group-focus-within/search:text-classic-gold" 
        />
        <input
          v-model.trim="searchQuery"
          type="text"
          class="w-full bg-transparent pr-11 pl-4 py-3.5 text-sm text-white placeholder-gray-500 focus:outline-none transition-all duration-300"
          placeholder="جستجوی مهارت..."
          autocomplete="off"
        >
      </div>

      <div 
        v-if="selectedSkills.length" 
        class="flex flex-wrap gap-2 p-3.5 border-b border-white/[0.08] bg-classic-gold/[0.02]"
      >
        <button
          v-for="skill in selectedSkills"
          :key="skill.id"
          type="button"
          class="inline-flex items-center gap-2 rounded-xl border border-classic-gold/30 bg-classic-gold/10 px-3 py-1.5 text-xs text-classic-gold font-medium transition-all duration-200 hover:bg-rose-500/10 hover:border-rose-500/30 hover:text-rose-400 group/chip shadow-sm"
          :title="`حذف ${skill.name}`"
          @click="$emit('toggle', skill)"
        >
          <img v-if="skill.icon" :src="resolveMediaUrl(skill.icon)" class="h-4 w-4 object-contain" alt="">
          <span>{{ skill.name }}</span>
          <Icon name="mdi:close" class="text-xs transition-transform duration-200 group-hover/chip:rotate-90 text-classic-gold/60 group-hover/chip:text-rose-400" />
        </button>
      </div>

      <div class="max-h-56 overflow-y-auto custom-skill-scrollbar">
        
        <div v-if="loading" class="py-10 text-center text-sm text-gray-400 flex flex-col items-center justify-center gap-3">
          <Icon name="mdi:loading" class="animate-spin text-classic-gold text-2xl" />
          <span class="font-medium">در حال دریافت مهارت‌ها...</span>
        </div>

        <div v-else-if="skills.length === 0" class="py-10 text-center text-sm text-gray-500 flex flex-col items-center justify-center gap-2">
          <Icon name="mdi:folder-search-outline" class="text-3xl text-gray-600" />
          <span class="font-medium">مهارتی پیدا نشد.</span>
        </div>

        <div v-else class="p-3.5 flex flex-wrap gap-2.5">
          <button
            v-for="skill in skills"
            :key="skill.id"
            type="button"
            class="flex items-center gap-2.5 rounded-xl border px-3 py-2 text-xs font-medium transition-all duration-300 group relative select-none"
            :class="isSelected(skill.id)
              ? 'border-classic-gold/40 bg-classic-gold/10 text-classic-gold font-semibold shadow-md shadow-classic-gold/5'
              : 'border-white/[0.06] bg-white/[0.04] text-gray-300 hover:bg-white/[0.08] hover:border-white/20 hover:text-white'"
            @click="$emit('toggle', skill)"
          >
            <img 
              v-if="skill.icon" 
              :src="resolveMediaUrl(skill.icon)" 
              class="h-6 w-6 object-contain flex-shrink-0 transition-transform duration-300 group-hover:scale-110" 
              :alt="skill.name"
            >
            <span class="whitespace-nowrap text-sm">{{ skill.name }}</span>
            <Icon 
              v-if="isSelected(skill.id)" 
              name="mdi:check" 
              class="text-classic-gold text-xs flex-shrink-0" 
            />
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * Dashboard/ProjectFormSkillSearch.vue
 * ─────────────────────────────────────────────────────────────────────────────
 * A responsive, real-time searchable skill picker component.
 * Features asynchronous data fetching with integrated debounce mechanism to 
 * limit unnecessary API load during typing.
 * Includes explicit separation between active chips and selectable options list.
 * ─────────────────────────────────────────────────────────────────────────────
 */

import { ref, watch, onBeforeUnmount } from 'vue'
import type { skillItem } from '~/models/Skill/SkillDTO'
import { getSkillsService } from '~/services/skills/skills.Service'
import { resolveMediaUrl } from '~/utilities/urlHelpers'

const props = defineProps<{
  selectedSkills: skillItem[]
}>()

defineEmits<{
  toggle: [skill: skillItem]
}>()

const searchQuery = ref('')
const skills = ref<skillItem[]>([])
const loading = ref(false)

/** Holds reference to active timeout window for query debouncing */
let debounceTimer: ReturnType<typeof setTimeout> | null = null

/** Checks if a specific skill is currently present in the selection list */
const isSelected = (id: number) => props.selectedSkills.some(s => s.id === id)

/** Performs backend search request using current search query state */
const loadSkills = async () => {
  loading.value = true
  try {
    const res = await getSkillsService(1, searchQuery.value)
    skills.value = res.data?.results ?? []
  } finally {
    loading.value = false
  }
}

/** Watches search updates; resets timer and executes callback after 280ms threshold */
watch(searchQuery, () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(loadSkills, 280)
}, { immediate: true })

/** Clears remaining scheduled timer allocations prior to teardown */
onBeforeUnmount(() => {
  if (debounceTimer) clearTimeout(debounceTimer)
})
</script>

<style scoped>
.custom-skill-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-skill-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-skill-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 999px;
}
.custom-skill-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.22);
}
</style>