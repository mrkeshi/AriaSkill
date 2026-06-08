<template>
  <NuxtLink
    :to="`/projects/pr-${project.slug}`"
    class="group h-full flex flex-col backdrop-blur-md bg-carb-gray/10 border border-white/10 rounded-2xl overflow-hidden transition-all duration-300 hover:-translate-y-1.5 hover:border-classic-gold/40 hover:shadow-[0_0_30px_rgba(212,175,55,0.25)]"
  >
    <div class="w-full h-48 relative overflow-hidden flex-shrink-0">
      <img
        :src="projectImage"
        :alt="project.title"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
      />
      <span class="absolute top-3 right-3 text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-lg bg-black/70 backdrop-blur-sm text-classic-gold border border-classic-gold/30 shadow-[0_0_10px_rgba(212,175,55,0.2)]">
        {{ project.project_type_display || project.project_type }}
      </span>
    </div>

    <div class="p-4 flex flex-col flex-1 gap-3">

      <h3 class="text-base font-bold text-white group-hover:text-classic-gold transition-colors duration-300 line-clamp-1 leading-snug">
        {{ project.title }}
      </h3>

      <div class="flex flex-wrap gap-1.5 min-h-[26px]">
        <span
          v-for="skill in project.skills.slice(0, 3)"
          :key="skill.id"
          class="flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-md bg-white/5 border border-white/10 text-gray-300 transition-colors duration-300 group-hover:border-white/20"
        >
          <img v-if="skill.icon" :src="resolveMediaUrl(skill.icon)" class="h-3.5 w-3.5 object-contain" :alt="skill.name" />
          <Icon v-else name="mdi:code-tags" class="h-3.5 w-3.5 text-classic-gold" />
          {{ skill.name }}
        </span>
        <span v-if="project.skills.length === 0" class="text-[11px] text-gray-600 italic">بدون مهارت</span>
      </div>

      <div class="flex items-center gap-1.5 text-[11px] text-gray-500">
        <Icon name="mdi:calendar" size="13" />
        <span>{{ toJalaliLong(project.created_at) }}</span>
      </div>

      <div class="flex-1"></div>

      <div class="pt-3 border-t border-white/5 flex items-center justify-between">
        <div class="flex items-center gap-4 text-gray-400">
          <span class="flex items-center gap-1 text-xs hover:text-rose-400 transition-colors">
            <Icon name="mdi:heart" class="text-rose-500 text-[15px] filter drop-shadow-[0_0_4px_rgba(244,63,94,0.5)]" />
            {{ toPersianNumerals(project.likes_count) }}
          </span>
          <span class="flex items-center gap-1 text-xs hover:text-indigo-400 transition-colors">
            <Icon name="mdi:download" class="text-indigo-400 text-[15px] filter drop-shadow-[0_0_4px_rgba(129,140,248,0.5)]" />
            {{ toPersianNumerals(project.download_count) }}
          </span>
        </div>

        <span class="w-8 h-8 rounded-full bg-classic-gold/10 border border-classic-gold/20 flex items-center justify-center text-classic-gold group-hover:bg-classic-gold group-hover:text-black group-hover:shadow-[0_0_15px_rgba(212,175,55,0.6)] transition-all duration-300">
          <Icon name="mdi:arrow-left" size="16" />
        </span>
      </div>

    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
/**
 * ProjectCard Component: Renders a compact, grid-friendly project card with high-contrast, cyberpunk-inspired dark aesthetics.
 * Features smooth glassmorphic hover effects, localized Jalali date conversion, and responsive icon fallbacks for associated tech skills.
 * Orchestrates structural layouts using Tailwind utility classes, capping skill badges at a maximum of three items for clean visuals.
 */
import type { PublicProjectMiniDTO } from '~/models/User/PublicProfileDTO'
import { toPersianNumerals, toJalaliLong } from '~/utilities/dateHelpers'
import { resolveMediaUrl } from '~/utilities/urlHelpers'

const props = defineProps<{
  project: PublicProjectMiniDTO
}>()

const projectImage = computed(() =>
  resolveMediaUrl(props.project.image) || '/images/project-1.jpg'
)
</script>