<template>
  <div>
    <SectionsHeroProject />

    <SectionsStats />

    <section class="max-w-7xl mx-auto px-4 md:px-8 py-12" dir="rtl">

      <div class="flex flex-col md:flex-row items-stretch gap-4 mb-10">
        <div class="flex-1 flex items-center gap-3 px-5 py-3 rounded-xl bg-black/20 backdrop-blur-md border border-white/10 hover:border-classic-gold/40 transition">
          <input
            v-model="quickSearch"
            type="text"
            maxlength="100"
            placeholder="جستجوی سریع بین پروژه‌ها..."
            class="flex-1 bg-transparent border-none outline-none text-bone-white placeholder-gray-400 text-md"
            @keyup.enter="goToFilter"
          />
          <button
            @click="goToFilter"
            class="w-12 h-12 flex items-center justify-center rounded-full bg-classic-gold/20 text-classic-gold hover:bg-classic-gold/30 transition cursor-pointer"
          >
            <Icon name="mdi:magnify" size="28" />
          </button>
        </div>

        <NuxtLink
          to="/projects/filter"
          class="flex items-center gap-2 px-6 py-3 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 hover:border-classic-gold/30 transition text-gray-300 text-sm"
        >
          <Icon name="mdi:filter-variant" size="20" />
          <span>رفتن به صفحه فیلتر پیشرفته</span>
        </NuxtLink>
      </div>

      <div class="mb-8">
        <h3 class="text-gray-400 text-sm mb-3">فیلتر سریع تکنولوژی:</h3>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="tech in quickTechnologies"
            :key="tech.slug"
            @click="toggleQuickTech(tech.slug)"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-sm transition cursor-pointer"
            :class="
              selectedTechs.includes(tech.slug)
                ? 'border-classic-gold bg-classic-gold/20 text-classic-gold'
                : 'border-white/10 bg-white/5 text-gray-300 hover:bg-white/10'
            "
          >
            <img v-if="tech.icon" :src="tech.icon" class="h-4 w-4 object-contain" :alt="tech.name" />
            <Icon v-else name="mdi:code-tags" size="16" class="text-gray-400" />
            {{ tech.name }}
          </button>

          <button
            v-if="techPending"
            v-for="i in 5"
            :key="i"
            class="h-8 w-20 rounded-lg bg-white/5 animate-pulse"
          />
        </div>
      </div>

      <div class="flex items-center justify-between mb-6 flex-wrap gap-3">
        <h2 class="text-xl font-bold text-white">
          <span class="text-classic-gold">{{ totalProjects }}</span>
          پروژه یافت شد
        </h2>
        <div class="flex gap-2 flex-wrap">
          <button
            v-for="s in sortOptions"
            :key="s.value"
            @click="activeSortOption = s.value; fetchProjects()"
            class="px-4 py-2 rounded-lg text-sm border transition"
            :class="
              activeSortOption === s.value
                ? 'border-classic-gold text-classic-gold bg-classic-gold/10'
                : 'border-white/10 text-gray-400 hover:bg-white/5'
            "
          >
            {{ s.label }}
          </button>
        </div>
      </div>

      <div v-if="projectsPending" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <SkeletonSimple v-for="i in 6" :key="i" class="h-72" />
      </div>

      <div
        v-else-if="projects.length === 0"
        class="py-24 flex flex-col items-center gap-4 text-gray-400"
      >
        <Icon name="mdi:folder-search-outline" size="56" class="opacity-40" />
        <p class="text-lg">پروژه‌ای با این فیلترها یافت نشد</p>
        <button @click="clearFilters" class="text-classic-gold underline text-sm mt-2">
          پاک کردن فیلترها
        </button>
      </div>

      <ProjectContainer v-else lg-grid="3" min :projects="projects" />

      <div class="flex items-center justify-center gap-3 mt-8" v-if="totalPages > 1">
        <button
          v-for="page in totalPages"
          :key="page"
          @click="currentPage = page; fetchProjects()"
          class="w-10 h-10 rounded-lg border text-sm transition"
          :class="
            currentPage === page
              ? 'border-classic-gold text-classic-gold bg-classic-gold/10'
              : 'border-white/10 text-gray-400 hover:bg-white/5'
          "
        >
          {{ page }}
        </button>
      </div>
    </section>
  </div>
</template>

<script lang="ts" setup>
// @page Explore 
// This page allows users to explore and discover various projects. It includes a search bar for quick filtering, a list of popular technologies for quick access, and sorting options to organize the displayed projects. The projects are fetched from the server based on the applied filters and sorting criteria, and pagination is implemented for easy navigation through multiple pages of projects. SEO metadata is generated to improve search engine visibility for this page.
import { getPublicProjectsService, getProjectYearsService } from '~/services/projects/project.Service'
import { getSkillsService } from '~/services/skills/skills.Service'
import { generateSeoMeta } from '~/utilities/seo'
import type { ProjectDTO } from '~/models/Project/ProjectDTO'
import type { skillItem } from '~/models/Skill/SkillDTO'

const router = useRouter()

const quickSearch = ref('')

const quickTechnologies = ref<skillItem[]>([])
const selectedTechs = ref<string[]>([])
const techPending = ref(true)


const sortOptions = [
  { label: 'جدیدترین', value: 'new' },
  { label: 'محبوب‌ترین', value: 'popular' },
  { label: 'بیشترین دانلود', value: 'downloads' },
  { label: 'قدیمی‌ترین', value: 'old' },
]
const activeSortOption = ref('new')


const projects = ref<ProjectDTO[]>([])
const projectsPending = ref(true)
const totalProjects = ref(0)
const currentPage = ref(1)
const pageSize = 9
const totalPages = computed(() => Math.ceil(totalProjects.value / pageSize))

const fetchProjects = async () => {
  projectsPending.value = true
  try {
    const res = await getPublicProjectsService(currentPage.value, pageSize, {
      q: quickSearch.value || undefined,
      technology: selectedTechs.value,
      sort: activeSortOption.value as any,
    })
    projects.value = res?.data?.results ?? []
    totalProjects.value = res?.data?.count ?? 0
  } catch (e) {
    console.error(e)
  } finally {
    projectsPending.value = false
  }
}

const toggleQuickTech = (slug: string) => {
  const idx = selectedTechs.value.indexOf(slug)
  if (idx === -1) selectedTechs.value.push(slug)
  else selectedTechs.value.splice(idx, 1)
  currentPage.value = 1
  fetchProjects()
}

const goToFilter = () => {
  const query: Record<string, string> = {}
  if (quickSearch.value) query.q = quickSearch.value
  if (selectedTechs.value.length) query.technology = selectedTechs.value.join(',')
  router.push({ path: '/projects/filter', query })
}

const clearFilters = () => {
  quickSearch.value = ''
  selectedTechs.value = []
  activeSortOption.value = 'new'
  currentPage.value = 1
  fetchProjects()
}

onMounted(async () => {

  techPending.value = true
  try {
    const res = await getSkillsService(1)

    quickTechnologies.value = (res?.data?.results ?? []).slice(0, 10)
  } catch (e) {
    console.error(e)
  } finally {
    techPending.value = false
  }

  await fetchProjects()
})

const seo = generateSeoMeta({
  title: 'اکتشاف پروژه‌ها',
  description: 'کشف هزاران پروژه واقعی در SkillSphere',
  image: '',
  url: '',
  keywords: ['اکتشاف پروژه', 'پروژه‌های برنامه‌نویسی'],
  author: 'علیرضا کشاورز',
  type: 'website',
})
useHead(seo)
</script>