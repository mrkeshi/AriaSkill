<template>
  <UiCardBlury>
    <Confirm
      v-model="deleteModal"
      title="حذف نظر"
      :description="deleteDescription"
      @confirm="confirmDelete"
    />

    <div class="transition-all" dir="rtl">

      <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between mb-6">
        <div>
          <h2 class="text-xl font-bold text-white tracking-wide">مدیریت نظرات</h2>
          <p class="text-sm text-gray-400 mt-1">مشاهده، جستجو، فعال‌سازی و حذف نظرات ثبت‌شده</p>
        </div>
        <span class="bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-3 py-1 rounded-full text-xs w-fit">
          {{ toPersianNumerals(totalCount) }} نظر
        </span>
      </div>

      <div class="flex flex-col gap-3 md:flex-row mb-5">
        <div class="relative flex-1">
          <Icon name="mdi:magnify" class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 text-xl" />
          <input
            v-model="searchInput"
            type="search"
            placeholder="جستجو بر اساس متن، نام کاربر یا عنوان پروژه"
            class="w-full rounded-xl border border-white/10 bg-white/5 py-3 pr-12 pl-4 text-white placeholder:text-gray-500 outline-none transition focus:border-classic-gold/60 focus:bg-white/10"
            @keyup.enter="submitSearch"
          >
        </div>

        <div class="flex gap-2">
          <button
            type="button"
            class="inline-flex items-center justify-center gap-2 rounded-xl bg-classic-gold px-5 py-3 text-sm font-bold text-slate-950 transition hover:bg-yellow-400"
            @click="submitSearch"
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
            پاک
          </button>
        </div>
      </div>

      <div class="flex p-0.5 bg-black/30 rounded-lg border border-white/10 w-fit mb-5">
        <button
          v-for="tab in statusTabs"
          :key="tab.value ?? 'all'"
          type="button"
          :class="[
            'px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200',
            activeStatus === tab.value
              ? 'bg-white/15 text-white shadow-lg'
              : 'text-gray-400 hover:text-gray-200',
          ]"
          @click="setStatusTab(tab.value)"
        >
          {{ tab.label }}
        </button>
      </div>

      <SkeletonSimple v-if="pending" :repeat="6" class="h-16 mb-2" />

      <div v-else class="overflow-x-auto rounded-xl border border-white/10 bg-white/[0.03] backdrop-blur-md shadow-inner">
        <table class="w-full text-right whitespace-nowrap">
          <thead class="bg-white/[0.04] text-gray-400 text-xs font-bold uppercase tracking-wider border-b border-white/10">
            <tr>
              <th class="p-4 text-center w-12">#</th>
              <th class="p-4">کاربر</th>
              <th class="p-4">پروژه</th>
              <th class="p-4">نظر</th>
              <th class="p-4 text-center">وضعیت</th>
              <th class="p-4 text-center">تاریخ</th>
              <th class="p-4 text-center">عملیات</th>
            </tr>
          </thead>

          <tbody class="text-gray-200 text-sm divide-y divide-white/[0.05]">
            <tr
              v-for="(item, index) in comments"
              :key="item.id"
              class="hover:bg-white/[0.04] transition-all duration-200 group"
              :class="{ 'opacity-50': item.status === 'inactive' }"
            >
              <td class="p-4 text-center text-gray-500  text-xs">
                {{ toPersianNumerals(rowNumber(index, currentPage, 10)) }}
              </td>

              <td class="p-4">
                <div class="flex items-center gap-3">
                  <div class="relative shrink-0">
                    <img
                      v-if="item.user_avatar"
                      :src="resolveMediaUrl(item.user_avatar)"
                      :alt="item.user_name"
                      class="w-9 h-9 rounded-full object-cover border border-white/20"
                    >
                    <div
                      v-else
                      class="w-9 h-9 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-300 flex items-center justify-center font-bold text-sm"
                    >
                      {{ firstLetter(item.user_name) }}
                    </div>
                  </div>
                  <span class="font-medium text-white/90 text-sm">{{ item.user_name }}</span>
                </div>
              </td>

              <td class="p-4">
                <NuxtLink
                  :to="`/projects/pr-${item.project_slug}`"
                  class="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-lg bg-classic-gold/10 text-classic-gold border border-classic-gold/20 hover:bg-classic-gold/20 transition max-w-[160px] truncate"
                  :title="item.project_title"
                >
                  <Icon name="mdi:open-in-new" class="shrink-0 text-xs" />
                  {{ item.project_title }}
                </NuxtLink>
              </td>

              <td class="p-4 text-gray-300 max-w-xs">
                <p class="truncate text-sm leading-relaxed" :title="item.message">{{ item.message }}</p>
                <span v-if="item.parent" class="text-[10px] text-cyan-400/70 mt-0.5 block">↩ پاسخ به نظر</span>
              </td>

              <td class="p-4 text-center">
                <span
                  class="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-full border"
                  :class="item.status === 'active'
                    ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
                    : 'bg-rose-500/10 text-rose-300 border-rose-500/30'"
                >
                  <span
                    class="w-1.5 h-1.5 rounded-full"
                    :class="item.status === 'active' ? 'bg-emerald-400' : 'bg-rose-400'"
                  ></span>
                  {{ item.status === 'active' ? 'فعال' : 'غیرفعال' }}
                </span>
              </td>

              <td class="p-4 text-center text-gray-400 text-xs">
                {{ toJalaliLong(item.created_at) }}
              </td>

              <td class="p-4">
                <div class="flex items-center justify-center gap-2">
                  <button
                    type="button"
                    :title="item.status === 'active' ? 'غیرفعال کردن' : 'فعال کردن'"
                    :disabled="actionLoadingId === item.id"
                    class="p-2 rounded-lg border transition inline-flex items-center justify-center disabled:opacity-40 disabled:cursor-not-allowed"
                    :class="item.status === 'active'
                      ? 'bg-amber-500/10 hover:bg-amber-500/20 border-amber-500/30 text-amber-300'
                      : 'bg-emerald-500/10 hover:bg-emerald-500/20 border-emerald-500/30 text-emerald-300'"
                    @click="toggleStatus(item)"
                  >
                    <Icon
                      v-if="actionLoadingId === item.id"
                      name="mdi:loading"
                      class="text-base animate-spin"
                    />
                    <Icon
                      v-else
                      :name="item.status === 'active' ? 'mdi:eye-off-outline' : 'mdi:eye-outline'"
                      class="text-base"
                    />
                  </button>

                  <button
                    type="button"
                    title="حذف"
                    :disabled="actionLoadingId === item.id"
                    class="p-2 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 text-rose-400 transition inline-flex items-center justify-center disabled:opacity-40 disabled:cursor-not-allowed"
                    @click="openDelete(item)"
                  >
                    <Icon name="mdi:trash-can-outline" class="text-base" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="comments.length === 0" class="p-12 text-center text-gray-500 flex flex-col items-center justify-center gap-3">
          <Icon name="mdi:comment-off-outline" class="text-4xl text-gray-600" />
          <span class="text-sm font-medium">نظری یافت نشد.</span>
        </div>
      </div>

      <div v-if="comments.length > 0" class="mt-6 flex justify-center">
        <UiPagination :totalPages="totalPages" />
      </div>

    </div>
  </UiCardBlury>
</template>

<script setup lang="ts">

/**
 * @component AdminCommentManagement
 * @description Back-office dashboard interface for managing project comments.
 * Provides comprehensive CRUD-like controls including search, filter, 
 * status activation toggle, and deletion workflows.
 * * @features
 * - Reactive Server-Side Pagination & Data Fetching via Nuxt `useAsyncData`.
 * - Dynamic filtering using query params via `statusTabs`.
 * - Multi-criteria search (message content, username, project title).
 * - Inline status toggling with independent loading states (`actionLoadingId`).
 * - Deep localization featuring RTL layout, Jalali date parsing, and Persian numerals.
 * * @composables
 * - `useAdminSearch`  : Manages debounced/triggered text filtering.
 * - `useCurrentPage`  : Synchronizes state with active pagination index.
 * - `useDeleteModal`  : Safe deletion context & state coordinator.
 */

import type { CommentManagementDTO } from '~/models/Comment/SendCommentDTO'
import {
  getAdminCommentsService,
  updateAdminCommentStatusService,
  deleteAdminCommentService,
} from '~/services/projects/project.Service'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { toJalaliLong, toPersianNumerals } from '~/utilities/dateHelpers'
import { resolveMediaUrl } from '~/utilities/urlHelpers'
import { firstLetter, rowNumber } from '~/utilities/stringHelpers'
import { useAdminSearch } from '~/composable/useAdminSearch'
import { useCurrentPage } from '~/composable/useCurrentPage'
import { useDeleteModal } from '~/composable/useDeleteModal'

definePageMeta({ layout: 'dashboard' })
useHead({ title: 'مدیریت نظرات' })

const route = useRoute()
const router = useRouter()
const { showInfo } = useCustomToastify()
const { searchInput, searchQuery, submitSearch, clearSearch } = useAdminSearch()

const { currentPage } = useCurrentPage()
const activeStatus = computed(() => (route.query.status as 'active' | 'inactive' | undefined) ?? undefined)
const { deleteModal, selectedItem: selectedComment, openDelete } = useDeleteModal<CommentManagementDTO>()
const actionLoadingId = ref<number | null>(null)

const statusTabs: { label: string; value: 'active' | 'inactive' | undefined }[] = [
  { label: 'همه', value: undefined },
  { label: 'فعال', value: 'active' },
  { label: 'غیرفعال', value: 'inactive' },
]

const { data, refresh, pending } = await useAsyncData(
  'admin-comments-list',
  () => getAdminCommentsService(currentPage.value, searchQuery.value, activeStatus.value),
  { watch: [currentPage, searchQuery, activeStatus] },
)

const comments = computed<CommentManagementDTO[]>(() => data.value?.data?.results ?? [])
const totalCount = computed(() => data.value?.data?.count ?? 0)
const totalPages = computed(() => Math.ceil(totalCount.value / 10))

const deleteDescription = computed(() => {
  const name = selectedComment.value?.user_name ?? ''
  return `آیا مطمئن هستید که می‌خواهید نظر «${name}» را حذف کنید؟`
})

const setStatusTab = (value: 'active' | 'inactive' | undefined) => {
  router.push({
    query: {
      ...route.query,
      page: undefined,
      status: value || undefined,
    },
  })
}

const toggleStatus = async (item: CommentManagementDTO) => {
  actionLoadingId.value = item.id
  try {
    const newStatus = item.status === 'active' ? 'inactive' : 'active'
    await updateAdminCommentStatusService(item.id, newStatus)
    showInfo({
      title: 'وضعیت تغییر کرد',
      message: newStatus === 'active' ? 'نظر فعال شد.' : 'نظر غیرفعال شد.',
    })
    await refresh()
  } finally {
    actionLoadingId.value = null
  }
}

const confirmDelete = async () => {
  if (!selectedComment.value) return
  actionLoadingId.value = selectedComment.value.id
  try {
    await deleteAdminCommentService(selectedComment.value.id)
    showInfo({ title: 'نظر حذف شد', message: 'نظر با موفقیت حذف شد.' })
    selectedComment.value = null
    await refresh()
  } finally {
    actionLoadingId.value = null
  }
}
</script>