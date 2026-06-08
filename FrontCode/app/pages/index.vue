<template>
  <SectionsHero />
  <SectionsHowWork />

  <section class="py-10">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl md:text-3xl font-semibold text-classic-gold">پروژه‌ها</h2>

      <UiButton variant="bracket" :to="{ path: '/projects/filter' }">
        بیشتر ببینید
      </UiButton>
    </div>

    <SkeletonSimple v-if="pending" :repeat="6" class="h-80 mb-4" />

    <ProjectContainer v-else-if="homeProjects.length" :projects="homeProjects" />

    <UiCardBlury v-else>
      <p class="text-center text-gray-400">هنوز پروژه‌ای برای نمایش وجود ندارد.</p>
    </UiCardBlury>
  </section>
</template>

<script setup lang="ts">
// @page Home
// This is the home page of the website, which includes a hero section, a how-it-works section, and a showcase of projects. The projects are fetched from the server and displayed in
import { getPublicProjectsService } from '~/services/projects/project.Service'
import { generateSeoMeta } from '~/utilities/seo'

const { data, pending } = await useAsyncData(
  'home-projects',
  () => getPublicProjectsService(1, 6),
)

const homeProjects = computed(() => {
  const projects = data.value?.data
  const list = Array.isArray(projects) ? projects : projects?.results ?? []
  return list.slice(0, 6)
})

useHead(generateSeoMeta({
  title: 'آریا کرافت ',
  description: 'نمایش پروژه‌های آریا اسکیل',
  image: '',
  url: '',
  keywords: ['پروژه', 'مهارت', 'آریا اسکیل'],
  author: 'آریا اسکیل',
  type: 'website',
}))
</script>
