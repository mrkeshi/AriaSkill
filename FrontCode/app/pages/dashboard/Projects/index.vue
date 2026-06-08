<template>
  <UiCardBlury>
    <Confirm
      v-model="deleteModal"
      title="حذف پروژه"
      description="آیا مطمئن هستید که می‌خواهید این پروژه را حذف کنید؟"
      @confirm="deleteSelectedProject"
    />

    <div class="space-y-6">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <h2 class="text-xl font-bold text-white tracking-wide" dir="rtl">
          پروژه‌های من
          <span class="bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-3 py-1 rounded-full text-sm mr-2">
      
            {{ toPersianNumerals(totalCount) }} پروژه
          </span>
        </h2>

        <UiButton variant="outline" :to="'/dashboard/projects/add'" icon="mdi:plus">
          پروژه جدید
        </UiButton>
      </div>

      <SkeletonSimple v-if="pending" :repeat="5" class="h-16 mb-2" />

  <div v-else class="overflow-x-auto rounded-2xl border border-white/10 bg-white/[0.03] backdrop-blur-xl shadow-2xl relative">
    <table class="w-full text-right whitespace-nowrap border-collapse" dir="rtl">
      <thead class="bg-white/[0.04] text-gray-400 text-xs font-bold uppercase tracking-wider border-b border-white/10">
        <tr>
          <th class="p-4 text-center w-12">#</th>
          <th class="p-4">پروژه</th>
          <th class="p-4">نوع</th>
          <th class="p-4">تاریخ ثبت</th>
          <th class="p-4">مهارت‌ها</th>
          <th class="p-4 text-center">تعداد دانلود</th>
          <th class="p-4 text-center">تعداد لایک</th>
          <th class="p-4 text-center">عملیات</th>
        </tr>
      </thead>

      <tbody class="text-gray-200 text-sm divide-y divide-white/[0.06]">
        <tr v-for="(item, index) in projects" :key="item.id" class="hover:bg-white/[0.05] transition-all duration-300 group">
          

          <td class="p-4 text-center text-gray-500  text-xs">{{ toPersianNumerals(rowNumber(index, currentPage, 6)) }}</td>

          <td class="p-4">
            <div class="font-semibold text-white group-hover:text-classic-gold transition-colors duration-200">
              {{ item.title }}
            </div>
          </td>

          <td class="p-4">
            <span class="inline-flex items-center px-2.5 py-1 text-xs font-medium rounded-full bg-classic-gold/10 text-classic-gold border border-classic-gold/30 shadow-sm shadow-classic-gold/5">
              {{ item.project_type_display || item.project_type }}
            </span>
          </td>

          <td class="p-4 text-gray-400 text-xs font-medium">
            {{ toJalali(item.created_at) }}
          </td>

          <td class="p-4">
            <div class="flex flex-wrap gap-1.5 max-w-xs sm:max-w-md">
              <span
                v-for="skill in item.skills"
                :key="skill.id"
                class="bg-white/[0.06] hover:bg-white/[0.12] border border-white/10 px-2 py-1 rounded-lg flex items-center gap-1.5 transition-all duration-200"
              >
                <img v-if="skill.icon" :src="resolveMediaUrl(skill.icon)" class="h-3.5 w-3.5 object-contain opacity-80 group-hover:opacity-100" :alt="skill.name">
                <span class="text-gray-300 text-[11px] font-medium">{{ skill.name }}</span>
              </span>
              <span v-if="item.skills.length === 0" class="text-xs text-gray-500 italic">بدون مهارت</span>
            </div>
          </td>


          <td class="p-4 text-center">
            <div class="inline-flex items-center gap-1 bg-emerald-500/5 border border-emerald-500/10 px-2.5 py-1 rounded-xl">
              <Icon name="mdi:download-outline" class="text-emerald-400 text-base" />
              <span class="font-semibold text-emerald-400  text-xs">{{ toPersianNumerals(item.download_count) }}</span>
            </div>
          </td>


          <td class="p-4 text-center">
            <div class="inline-flex items-center gap-1 bg-amber-500/5 border border-amber-500/10 px-2.5 py-1 rounded-xl">
              <Icon name="mdi:heart-outline" class="text-amber-400 text-base group-hover:scale-110 transition-transform" />
              <span class="font-semibold text-amber-400 text-xs">{{ toPersianNumerals(item.likes_count) }}</span>
            </div>
          </td>

          <td class="p-4 text-center">
            <div class="flex items-center justify-center gap-2">
              <NuxtLink
                :to="`/projects/pr-${item.slug}`"
                title="مشاهده"
                class="bg-white/5 hover:bg-white/10 hover:text-white border border-white/10 p-2 rounded-xl text-gray-400 transition-all duration-200 shadow-sm"
              >
                <Icon name="mdi:eye" class="text-base -mb-1" />
              </NuxtLink>

              <NuxtLink
                :to="`/dashboard/projects/edit-${item.slug}`"
                title="ویرایش"
                class="bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/20 p-2 rounded-xl text-blue-400 transition-all duration-200 shadow-sm"
              >
                <Icon name="mdi:pencil-outline" class="text-base  -mb-1" />
              </NuxtLink>

              <button
                title="حذف"
                class="bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/20 p-2 rounded-xl text-rose-400 transition-all duration-200 shadow-sm"
                @click="openDelete(item.slug)"
              >
                <Icon name="mdi:trash-can-outline" class="text-base  -mb-1" />
              </button>
            </div>
          </td>

        </tr>
      </tbody>
    </table>

    <div v-if="projects.length === 0" class="p-12 text-center text-gray-500 flex flex-col items-center justify-center gap-2">
      <Icon name="mdi:folder-open-outline" class="text-4xl text-gray-600" />
      <span class="text-sm font-medium">هیچ پروژه‌ای یافت نشد.</span>
    </div>
  </div>

      <UiPagination :totalPages="totalPages" />
    </div>
  </UiCardBlury>
</template>

<script setup lang="ts">
/**
 * @page MyProjectsListRegistry
 * @description Administrative control deck displaying ownership matrices, media resolutions, and localized project listings.
 * 
 * @logic_flow
 * - Isolated Destructions: Binds deletion confirmation loops to unique token strings (`string` slugs) rather than sequential primary keys.
 * - Grid Architecture: Limits datasets to compact 6-row increments, utilizing computed pagination thresholds (`totalCount / 6`).
 * - Row Counter Tracking: Implements standard global index trackers (`rowNumber`) to preserve table sequences across distinct data pages.
 * 
 * @composable_dependencies
 * - `useCurrentPage` : Hooks structural route indices automatically into underlying network reactive loops.
 * - `useDeleteModal`: Tracks modal presentation states and locks single entity parameters awaiting API validation.
 */
import { computed, ref } from 'vue'
import { deleteProjectService, getMyProjectsService } from '~/services/projects/project.Service'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { resolveMediaUrl } from '~/utilities/urlHelpers'
import { generateSeoMeta } from '~/utilities/seo'
import { toJalali, toPersianNumerals } from '~/utilities/dateHelpers'
import { rowNumber } from '~/utilities/stringHelpers'
import { useCurrentPage } from '~/composable/useCurrentPage'
import { useDeleteModal } from '~/composable/useDeleteModal'

definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const { currentPage } = useCurrentPage()
const { deleteModal, selectedItem: selectedSlug, openDelete } = useDeleteModal<string>()
const { showInfo } = useCustomToastify()

const { data, refresh, pending } = await useAsyncData(
  'my-projects',
  () => getMyProjectsService(currentPage.value),
  { watch: [currentPage] }
)

const projects = computed(() => data.value?.data?.results ?? [])
const totalCount = computed(() => data.value?.data?.count ?? 0)
const totalPages = computed(() => Math.ceil(totalCount.value / 6))

const deleteSelectedProject = async () => {
  if (!selectedSlug.value) return
  await deleteProjectService(selectedSlug.value)
  showInfo({ title: 'پروژه حذف شد', message: 'پروژه با موفقیت حذف شد.' })
  selectedSlug.value = null
  await refresh()
}

useHead(generateSeoMeta({
  title: 'پروژه‌های من',
  description: 'مدیریت پروژه‌ها',
  image: '',
  url: '',
  keywords: ['پروژه'],
  author: 'AriaSkill',
  type: 'website',
}))
</script>