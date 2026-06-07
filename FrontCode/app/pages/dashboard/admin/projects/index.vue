<template>
  <UiCardBlury>
    <Confirm
      v-model="deleteModal"
      title="حذف پروژه"
      :description="deleteDescription"
      @confirm="deleteSelectedProject"
    />

    <div class="transition-all" dir="rtl">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between mb-6">
        <div>
          <h2 class="text-xl font-bold text-white tracking-wide">مدیریت پروژه‌ها</h2>
          <p class="text-sm text-gray-400 mt-2">مشاهده، جستجو و مدیریت وضعیت پروژه‌های ثبت شده</p>
        </div>

        <span class="bg-cyan-400/10 text-cyan-300 border border-cyan-400/30 px-3 py-1 rounded-full text-xs w-fit">
          {{ toPersianNumerals(totalCount) }} پروژه
        </span>
      </div>

      <form class="mb-5 flex flex-col gap-3 md:flex-row" @submit.prevent="submitSearch">
        <div class="relative flex-1">
          <Icon name="mdi:magnify" class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 text-xl" />
          <input
            v-model="searchInput"
            type="search"
            placeholder="جستجو بر اساس عنوان، توضیحات، مالک، مهارت یا وضعیت"
            class="w-full rounded-xl border border-white/10 bg-white/5 py-3 pr-12 pl-4 text-white placeholder:text-gray-500 outline-none transition focus:border-classic-gold/60 focus:bg-white/10"
          >
        </div>

        <div class="flex gap-2">
          <button
            type="submit"
            class="inline-flex items-center justify-center gap-2 rounded-xl bg-classic-gold px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-yellow-400"
          >
            <Icon name="mdi:magnify" class="text-lg" />
            جستجو
          </button>
          <button
            v-if="searchQuery"
            type="button"
            class="inline-flex items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-5 py-3 text-sm font-bold text-gray-300 transition hover:bg-white/10"
            @click="clearSearch"
          >
            <Icon name="mdi:close" class="text-lg" />
            پاک کردن
          </button>
        </div>
      </form>

      <SkeletonSimple v-if="pending" :repeat="5" class="h-16 mb-2" />

      <div v-else class="overflow-x-auto rounded-xl border border-white/10 bg-white/5 backdrop-blur-md shadow-inner">
        <table class="w-full text-right whitespace-nowrap">
          <thead class="bg-white/5 text-gray-300 text-sm border-b border-white/10">
            <tr>
              <th class="p-4 font-medium w-16">#</th>
              <th class="p-4 font-medium">پروژه</th>
              <th class="p-4 font-medium">مالک</th>
              <th class="p-4 font-medium">نوع</th>
              <th class="p-4 font-medium">وضعیت</th>
              <th class="p-4 font-medium">آمار</th>
              <th class="p-4 font-medium">تاریخ ثبت</th>
              <th class="p-4 font-medium">عملیات</th>
            </tr>
          </thead>

          <tbody class="text-gray-200 text-sm divide-y divide-white/5">
            <tr
              v-for="(item, index) in projects"
              :key="item.id"
              class="hover:bg-white/5 transition duration-200 group"
            >
              <td class="p-4 text-gray-500 group-hover:text-gray-400 transition">
                {{ toPersianNumerals(rowNumber(index, currentPage.value, pageSize)) }}
              </td>

              <td class="p-4">
                <div class="flex items-center gap-3">
                  <div class="h-12 w-16 overflow-hidden rounded-xl border border-white/10 bg-white/5 flex items-center justify-center text-cyan-300">
                    <img
                      v-if="item.image"
                      :src="resolveMediaUrl(item.image)"
                      :alt="item.title"
                      class="h-full w-full object-cover"
                    >
                    <Icon v-else name="mdi:image-outline" class="text-2xl" />
                  </div>
                  <div class="min-w-0">
                    <p class="font-medium text-white/90 max-w-[240px] truncate" :title="item.title">{{ item.title }}</p>
                    <p class="text-xs text-gray-500 dir-ltr text-left max-w-[240px] truncate">{{ item.slug }}</p>
                  </div>
                </div>
              </td>

              <td class="p-4">
                <div class="flex items-center gap-3">
                  <div class="h-10 w-10 overflow-hidden rounded-xl border border-white/10 bg-white/5 flex items-center justify-center text-indigo-300">
                    <img
                      v-if="item.user.avatar"
                      :src="resolveMediaUrl(item.user.avatar)"
                      :alt="item.user.full_name"
                      class="h-full w-full object-cover"
                    >
                    <span v-else class="text-sm font-bold">{{ firstLetter(item.user.full_name || item.user.username) }}</span>
                  </div>
                  <div>
                    <p class="font-medium text-white/90">{{ item.user.full_name || item.user.username }}</p>
                    <p class="text-xs text-gray-500 dir-ltr text-left">{{ item.user.username }}</p>
                  </div>
                </div>
              </td>

              <td class="p-4">
                <span class="inline-flex items-center px-2.5 py-1 text-xs font-medium rounded-md bg-classic-gold/10 text-classic-gold border border-classic-gold/30">
                  {{ item.project_type_display || item.project_type }}
                </span>
              </td>

              <td class="p-4">
                <span :class="projectStatusClass(item.status)" class="inline-flex items-center gap-2 px-2 py-1 rounded-md border text-xs">
                  <span class="h-2 w-2 rounded-full" :class="projectStatusDotClass(item.status)"></span>
                  {{ projectStatusLabel(item.status) }}
                </span>
              </td>

              <td class="p-4">
                <div class="flex items-center gap-2">
                  <span class="inline-flex items-center gap-1 bg-emerald-500/5 border border-emerald-500/10 px-2 py-1 rounded-lg text-emerald-400 text-xs">
                    <Icon name="mdi:download-outline" class="text-base" />
                    {{ toPersianNumerals(item.download_count) }}
                  </span>
                  <span class="inline-flex items-center gap-1 bg-amber-500/5 border border-amber-500/10 px-2 py-1 rounded-lg text-amber-400 text-xs">
                    <Icon name="mdi:heart-outline" class="text-base" />
                    {{ toPersianNumerals(item.likes_count) }}
                  </span>
                  <span class="inline-flex items-center gap-1 bg-cyan-500/5 border border-cyan-500/10 px-2 py-1 rounded-lg text-cyan-400 text-xs">
                    <Icon name="mdi:eye-outline" class="text-base" />
                    {{ toPersianNumerals(item.view_count) }}
                  </span>
                </div>
              </td>

              <td class="p-4 text-gray-400">{{ toJalali(item.created_at) }}</td>

              <td class="p-4">
                <div class="flex gap-2">
                  <NuxtLink
                    :to="`/projects/pr-${item.slug}`"
                    title="مشاهده"
                    class="bg-white/5 hover:bg-white/10 border border-white/10 p-2 rounded-lg text-gray-400 hover:text-white transition inline-flex items-center justify-center"
                  >
                    <Icon name="mdi:eye-outline" class="text-lg" />
                  </NuxtLink>

                  <button
                    type="button"
                    class="border p-2 rounded-lg transition inline-flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
                    :class="isActiveProject(item) ? 'bg-amber-500/10 hover:bg-amber-500/20 border-amber-500/30 text-amber-300' : 'bg-emerald-500/10 hover:bg-emerald-500/20 border-emerald-500/30 text-emerald-300'"
                    :disabled="statusLoadingSlug === item.slug"
                    :title="isActiveProject(item) ? 'غیرفعال کردن' : 'فعال کردن'"
                    @click="toggleStatus(item)"
                  >
                    <Icon v-if="statusLoadingSlug === item.slug" name="mdi:loading" class="text-lg animate-spin" />
                    <Icon v-else :name="isActiveProject(item) ? 'mdi:close-circle-outline' : 'mdi:check-circle-outline'" class="text-lg" />
                  </button>

                  <button
                    type="button"
                    class="bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 p-2 rounded-lg text-rose-400 transition inline-flex items-center justify-center"
                    title="حذف پروژه"
                    @click="openDelete(item)"
                  >
                    <Icon name="mdi:trash-can-outline" class="text-lg" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="projects.length === 0" class="p-8 text-center text-gray-500 flex flex-col items-center gap-3">
          <Icon name="mdi:folder-search-outline" class="text-4xl text-gray-600" />
          <p>پروژه‌ای یافت نشد.</p>
        </div>
      </div>

      <div v-if="projects.length > 0" class="mt-6 flex justify-center">
        <UiPagination :totalPages="totalPages" />
      </div>
    </div>
  </UiCardBlury>
</template>

<script setup lang="ts">
import type { ProjectDTO } from '~/models/Project/ProjectDTO'
import { deleteAdminProjectService, getAdminProjectsService, updateAdminProjectStatusService } from '~/services/projects/project.Service'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { toJalali, toPersianNumerals } from '~/utilities/dateHelpers'
import { resolveMediaUrl } from '~/utilities/urlHelpers'
import { projectStatusLabel, projectStatusClass, projectStatusDotClass } from '~/utilities/projectHelpers'
import { firstLetter, rowNumber } from '~/utilities/stringHelpers'
import { useAdminSearch } from '~/composable/useAdminSearch'
import { useDeleteModal } from '~/composable/useDeleteModal'
import { useCurrentPage } from '~/composable/useCurrentPage'

definePageMeta({ layout: 'dashboard' })
useHead({ title: 'مدیریت پروژه‌ها' })

const route = useRoute()
const { showInfo } = useCustomToastify()
const { searchInput, searchQuery, submitSearch, clearSearch } = useAdminSearch()
const { currentPage } = useCurrentPage()
const { deleteModal, selectedItem: selectedProject, openDelete } = useDeleteModal<ProjectDTO>()

const pageSize = 6
const statusLoadingSlug = ref<string | null>(null)

const { data, refresh, pending } = await useAsyncData(
  'admin-projects-list',
  () => getAdminProjectsService(currentPage.value, searchQuery.value),
  {
    watch: [currentPage, searchQuery],
  },
)

const projects = computed<ProjectDTO[]>(() => data.value?.data?.results || [])
const totalCount = computed(() => data.value?.data?.count || 0)
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))
const deleteDescription = computed(() => {
  const title = selectedProject.value?.title || ''
  return `آیا برای حذف پروژه ${title} مطمئن هستید؟`
})

const isActiveProject = (project: ProjectDTO) => project.status === 'approved'

const deleteSelectedProject = async () => {
  if (!selectedProject.value) return
  await deleteAdminProjectService(selectedProject.value.slug)
  showInfo({ title: 'حذف پروژه', message: 'پروژه با موفقیت حذف شد.' })
  selectedProject.value = null
  await refresh()
}

const toggleStatus = async (project: ProjectDTO) => {
  statusLoadingSlug.value = project.slug
  try {
    await updateAdminProjectStatusService(project.slug, !isActiveProject(project))
    showInfo({
      title: 'وضعیت پروژه',
      message: isActiveProject(project) ? 'پروژه غیرفعال شد.' : 'پروژه فعال شد.',
    })
    await refresh()
  } finally {
    statusLoadingSlug.value = null
  }
}
</script>
