<template>
  <!-- اضافه شدن h-full و flex flex-col -->
  <div class="h-full flex flex-col backdrop-blur-md shadow-2xl bg-carb-gray/10 border border-white/10 rounded-2xl p-4 transition overflow-hidden hover:-translate-y-1 ease-in">

    <div class="w-full h-60 relative flex-shrink-0" v-show="!min">
      <img :src="projectImage" :alt="project.title" class="w-full h-full rounded-2xl object-cover">
      <span class="absolute bg-black -bottom-8 transition right-4 h-20 w-20 rounded-full border-[3px] border-classic-gold"></span>
      <img :src="authorAvatar" :alt="project.user.full_name" class="absolute -bottom-8 hover:opacity-60 transition right-4 h-20 w-20 rounded-full border-[3px] border-classic-gold object-cover">
    </div>

    <div :class="['p-2','md:p-4','flex','flex-col','flex-1',{ 'mt-7': !min }]">
      
      <NuxtLink :to="projectLink" class="text-xl transition hover:text-light-gold font-semibold text-white mb-1">
        {{ project.title }}
      </NuxtLink>
      <span class="text-gray-500">{{ project.project_type_display || project.project_type }}</span>
      
      <div class="my-3 h-0.5 bg-carb-gray/90 w-full"></div>
      
      <div class="flex flex-wrap gap-2">
        <span v-for="skill in visibleSkills" :key="skill.id" class="backdrop-blur-md shadow-xl p-2 transition hover:bg-carb-gray bg-carb-gray/40 border border-white/10 rounded-md flex items-center gap-1.5">
          <img v-if="skill.icon" :src="resolveMediaUrl(skill.icon)" class="h-5 w-5 object-contain" :alt="skill.name">
          <Icon v-else name="mdi:code-tags" class="h-5 w-5 text-classic-gold" />
          <span class="text-white text-sm">{{ skill.name }}</span>
        </span>
        <span v-if="visibleSkills.length === 0" class="text-gray-500 text-sm">بدون مهارت</span>
      </div>

      <div class="inline-flex backdrop-blur-md shadow-xl my-3 p-2 bg-carb-gray/40 border border-white/10 rounded-md items-center gap-1.5 w-fit">
        <Icon name="mdi:calendar" class="text-xl"/>
        <span class="text-white text-sm">{{ toJalaliLong(project.created_at) }}</span>
      </div>

      <div class="mt-auto">
        <div class="my-3 mt-0 mb-5 h-0.5 bg-carb-gray/90 w-full"></div>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4 text-gray-300">
            <span class="flex items-center gap-1 text-sm">
              <Icon name="mdi:heart" class="text-error text-[18px]" />
              {{ project.likes_count }} پسند
            </span>
            <span class="flex items-center gap-1 text-sm">
              <Icon name="mdi:download" class="text-indigo-600 text-[18px]" />
              {{ project.download_count }} دانلود
            </span>
          </div>

          <NuxtLink :to="projectLink" class="bg-classic-gold hover:bg-light-gold transition h-12 w-12 text-black rounded-full flex items-center justify-center">
            <Icon name="mdi:arrow-left" class="w-7 h-7" />
          </NuxtLink>
        </div>
      </div>

    </div>
  </div>
</template>


<script lang="ts" setup>
/**
 * - Implements a highly scalable glassmorphic asset/project display node canvas.
 * - Handles adaptive state transformations via structural responsive minimization flags.
 * - Caps relational taxonomy chip collections maximizing strict performance grid boundaries.
 */
import type { ProjectDTO } from '~/models/Project/ProjectDTO'
import { toJalaliLong } from '~/utilities/dateHelpers'
import { resolveMediaUrl } from '~/utilities/urlHelpers'

const props=defineProps<{
  project: ProjectDTO
  min?: boolean
}>()

const projectLink = computed(() => `/projects/pr-${props.project.slug}`)
const projectImage = computed(() => resolveMediaUrl(props.project.image) || '/images/project-1.jpg')
const authorAvatar = computed(() => resolveMediaUrl(props.project.user?.avatar) || '/images/user1.jpg')
const visibleSkills = computed(() => props.project.skills?.slice(0, 3) ?? [])
</script>
