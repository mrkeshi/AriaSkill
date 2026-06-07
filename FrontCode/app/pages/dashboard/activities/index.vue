<template>
  <UiCardBlury>
    <Confirm
      v-model="deleteModal"
      title="حذف فعالیت"
      description="آیا مطمئن هستید که می‌خواهید این فعالیت را حذف کنید؟"
      @confirm="handleDelete"
    />

    <div class="space-y-6" dir="rtl">

      <div class="flex flex-wrap items-center justify-between gap-3">
        <h2 class="text-xl font-bold text-white tracking-wide">
          تاریخچه فعالیت‌ها
          <span class="bg-amber-500/20 text-amber-300 border border-amber-500/30 px-3 py-1 rounded-full text-xs mr-2">
            {{ toPersianNumerals(totalCount) }} فعالیت
          </span>
        </h2>
        <button
          v-if="unseenCount > 0"
          type="button"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-sm border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 transition-all duration-200"
          :disabled="markAllLoading"
          @click="handleMarkAllSeen"
        >
          <Icon name="mdi:check-all" size="16" />
          <span>{{ markAllLoading ? 'در حال انجام...' : 'علامت‌گذاری همه به عنوان دیده‌شده' }}</span>
        </button>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <div class="flex p-0.5 bg-black/30 rounded-lg border border-white/10 backdrop-blur-sm">
          <button
            v-for="tab in seenTabs"
            :key="tab.key"
            type="button"
            :class="[
              'px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200',
              activeSeenKey === tab.key
                ? 'bg-white/15 text-white shadow-lg'
                : 'text-gray-400 hover:text-gray-200',
            ]"
            @click="setSeenTab(tab)"
          >
            {{ tab.label }}
            <span
              v-if="tab.key === 'unseen' && unseenCount > 0"
              class="mr-1.5 px-1.5 py-0.5 rounded-full bg-classic-gold text-black text-[11px] font-bold"
            >
              {{ toPersianNumerals(unseenCount) }}
            </span>
          </button>
        </div>

        <select
          v-model="activeType"
          class="bg-black/30 border border-white/10 text-gray-300 text-sm rounded-lg px-3 py-2 outline-none focus:border-classic-gold/40 transition"
          @change="resetPage"
        >
          <option value="">همه انواع</option>
          <option v-for="t in activityTypes" :key="t.value" :value="t.value">{{ t.label }}</option>
        </select>
      </div>

      <SkeletonSimple v-if="pending" :repeat="8" class="h-16 mb-2" />

      <div v-else-if="activities.length === 0" class="flex flex-col items-center justify-center py-16 text-gray-500 gap-3">
        <Icon name="mdi:history" class="text-5xl text-gray-600" />
        <span class="text-sm font-medium">هیچ فعالیتی یافت نشد.</span>
      </div>

      <div v-else class="flex flex-col gap-2">
        <div
          v-for="activity in activities"
          :key="activity.id"
          class="group flex items-center gap-3 p-3 rounded-xl border transition-all duration-200 backdrop-blur-md"
          :class="rowClass(activity.is_seen)"
        >
          <div
            class="shrink-0 flex items-center justify-center w-10 h-10 rounded-xl border"
            :class="typeStyle(activity.type).iconContainer"
          >
            <Icon :name="typeStyle(activity.type).icon" class="text-lg" />
          </div>

          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-0.5 flex-wrap">
              <span
                class="text-[10px] px-2 py-0.5 rounded-full font-bold whitespace-nowrap border"
                :class="typeStyle(activity.type).badge"
              >
                {{ typeStyle(activity.type).label }}
              </span>
              <h3 class="text-sm text-gray-100 font-semibold truncate">{{ activity.title }}</h3>
              <span v-if="!activity.is_seen" class="w-2 h-2 rounded-full bg-classic-gold shrink-0"></span>
              <span v-else class="text-[9px] text-gray-600 border border-white/5 px-1.5 py-0.5 rounded-full">خوانده‌شده</span>
            </div>
            <p class="text-[12px] text-gray-400 leading-relaxed line-clamp-1">{{ activity.description }}</p>
            <div class="flex items-center gap-1 mt-1 text-gray-600 text-[11px]">
              <Icon name="mdi:clock-outline" size="11" />
              <span>{{ toJalaliWithTime(activity.created_at) }}</span>
              <template v-if="activity.related_project_slug">
                <span class="mx-1 text-white/10">·</span>
                <NuxtLink
                  :to="`/projects/pr-${activity.related_project_slug}`"
                  class="text-classic-gold/70 hover:text-classic-gold transition-colors truncate max-w-[160px]"
                >
                  {{ activity.related_project_title }}
                </NuxtLink>
              </template>
            </div>
          </div>

          <div class="shrink-0 flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <button
              v-if="!activity.is_seen"
              type="button"
              title="علامت‌گذاری به عنوان دیده‌شده"
              class="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/20 transition-colors"
              :disabled="loadingId === activity.id"
              @click="handleMarkSeen(activity)"
            >
              <Icon name="mdi:check-all" class="text-sm" />
            </button>
            <button
              type="button"
              title="حذف"
              class="p-2 rounded-lg bg-rose-500/10 text-rose-400 border border-rose-500/30 hover:bg-rose-500/20 transition-colors"
              :disabled="loadingId === activity.id"
              @click="openDelete(activity.id)"
            >
              <Icon name="mdi:trash-can-outline" class="text-sm" />
            </button>
          </div>
        </div>
      </div>

      <UiPagination :totalPages="totalPages" />
    </div>
  </UiCardBlury>
</template>

<script setup lang="ts">
import type { ActivityDTO, ActivityType } from '~/models/Activity/ActivityDTO'
import {
  deleteActivityService,
  getActivitiesService,
  getUnseenActivityCountService,
  markActivitySeenService,
  markAllActivitiesSeenService,
} from '~/services/activity/activity.Service'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { generateSeoMeta } from '~/utilities/seo'
import { toPersianNumerals, toJalaliWithTime } from '~/utilities/dateHelpers'

definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const router = useRouter()
const { showInfo } = useCustomToastify()

const currentPage = computed(() => Number(route.query.page) || 1)

type SeenKey = 'all' | 'unseen' | 'seen'

const seenTabs: { key: SeenKey; label: string; value: boolean | undefined }[] = [
  { key: 'all', label: 'همه', value: undefined },
  { key: 'unseen', label: 'دیده‌نشده', value: false },
  { key: 'seen', label: 'دیده‌شده', value: true },
]

const activeSeenKey = ref<SeenKey>('all')
const activeSeenValue = computed(() => seenTabs.find(t => t.key === activeSeenKey.value)?.value)

const activeType = ref<ActivityType | ''>('')
const deleteModal = ref(false)
const selectedId = ref<number | null>(null)
const loadingId = ref<number | null>(null)
const markAllLoading = ref(false)

const activityTypes: { value: ActivityType; label: string }[] = [
  { value: 'login_success', label: 'ورود موفق' },
  { value: 'login_failed', label: 'ورود ناموفق' },
  { value: 'project_published', label: 'انتشار پروژه' },
  { value: 'project_created', label: 'ایجاد پروژه' },
  { value: 'project_updated', label: 'ویرایش پروژه' },
  { value: 'project_deleted', label: 'حذف پروژه' },
  { value: 'password_changed', label: 'تغییر رمز عبور' },
  { value: 'project_documentation_downloaded', label: 'دانلود مستندات' },
  { value: 'external_project_comment_created', label: 'دیدگاه در پروژه دیگران' },
  { value: 'comment_created', label: 'ثبت دیدگاه' },
]

const { data, pending, refresh } = await useAsyncData(
  'activities-list',
  () => getActivitiesService(currentPage.value, activeType.value || undefined, activeSeenValue.value),
  { watch: [currentPage, activeSeenKey, activeType] },
)

const { data: unseenData, refresh: refreshUnseen } = await useAsyncData(
  'activity-unseen-count',
  () => getUnseenActivityCountService(),
)

const activities = computed<ActivityDTO[]>(() => data.value?.data?.results ?? [])
const totalCount = computed(() => data.value?.data?.count ?? 0)
const totalPages = computed(() => Math.ceil(totalCount.value / 10))
const unseenCount = computed(() => unseenData.value?.data?.unseen_count ?? 0)

const rowClass = (isSeen: boolean) => {
  if (activeSeenKey.value === 'all') {
    return isSeen
      ? 'bg-white/[0.02] border-white/5 hover:bg-white/[0.04] hover:border-white/10'
      : 'bg-gradient-to-r from-white/[0.06] to-white/[0.03] border-white/10 hover:border-white/20 shadow-md'
  }
  return isSeen
    ? 'bg-white/[0.02] border-white/5 hover:bg-white/[0.04] hover:border-white/10'
    : 'bg-gradient-to-r from-white/[0.06] to-white/[0.03] border-white/10 hover:border-white/20 shadow-md'
}

const typeStyle = (type: ActivityType) => {
  const map: Record<ActivityType, { icon: string; label: string; iconContainer: string; badge: string }> = {
    login_success: {
      icon: 'mdi:login',
      label: 'ورود موفق',
      iconContainer: 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400',
      badge: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    },
    login_failed: {
      icon: 'mdi:shield-alert-outline',
      label: 'ورود ناموفق',
      iconContainer: 'border-rose-500/30 bg-rose-500/10 text-rose-400',
      badge: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
    },
    project_published: {
      icon: 'mdi:cloud-upload',
      label: 'انتشار پروژه',
      iconContainer: 'border-cyan-500/20 bg-cyan-500/10 text-cyan-400',
      badge: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
    },
    project_created: {
      icon: 'mdi:folder-plus-outline',
      label: 'ایجاد پروژه',
      iconContainer: 'border-cyan-500/20 bg-cyan-500/10 text-cyan-400',
      badge: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
    },
    project_updated: {
      icon: 'mdi:pencil-outline',
      label: 'ویرایش پروژه',
      iconContainer: 'border-blue-500/20 bg-blue-500/10 text-blue-400',
      badge: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    },
    project_deleted: {
      icon: 'mdi:folder-remove-outline',
      label: 'حذف پروژه',
      iconContainer: 'border-rose-500/20 bg-rose-500/10 text-rose-400',
      badge: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
    },
    password_changed: {
      icon: 'mdi:lock-reset',
      label: 'تغییر رمز',
      iconContainer: 'border-amber-500/20 bg-amber-500/10 text-amber-400',
      badge: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    },
    project_documentation_downloaded: {
      icon: 'mdi:file-download-outline',
      label: 'دانلود مستندات',
      iconContainer: 'border-purple-500/20 bg-purple-500/10 text-purple-400',
      badge: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    },
    external_project_comment_created: {
      icon: 'mdi:comment-arrow-left-outline',
      label: 'دیدگاه در پروژه دیگران',
      iconContainer: 'border-indigo-500/20 bg-indigo-500/10 text-indigo-400',
      badge: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20',
    },
    comment_created: {
      icon: 'mdi:comment-text-outline',
      label: 'ثبت دیدگاه',
      iconContainer: 'border-teal-500/20 bg-teal-500/10 text-teal-400',
      badge: 'bg-teal-500/10 text-teal-400 border-teal-500/20',
    },
  }
  return map[type] ?? {
    icon: 'mdi:information-outline',
    label: 'عمومی',
    iconContainer: 'border-white/10 bg-white/5 text-gray-400',
    badge: 'bg-white/10 text-gray-400 border-white/10',
  }
}

const setSeenTab = (tab: typeof seenTabs[number]) => {
  activeSeenKey.value = tab.key
  resetPage()
}

const resetPage = () => {
  router.push({ query: { ...route.query, page: 1 } })
}

const handleMarkSeen = async (activity: ActivityDTO) => {
  loadingId.value = activity.id
  try {
    await markActivitySeenService(activity.id, true)
    activity.is_seen = true
    await refreshUnseen()
  } finally {
    loadingId.value = null
  }
}

const openDelete = (id: number) => {
  selectedId.value = id
  deleteModal.value = true
}

const handleDelete = async () => {
  if (!selectedId.value) return
  loadingId.value = selectedId.value
  try {
    await deleteActivityService(selectedId.value)
    showInfo({ title: 'فعالیت حذف شد', message: 'فعالیت با موفقیت حذف شد.' })
    await refresh()
    await refreshUnseen()
  } finally {
    loadingId.value = null
    selectedId.value = null
  }
}

const handleMarkAllSeen = async () => {
  markAllLoading.value = true
  try {
    await markAllActivitiesSeenService()
    showInfo({ title: 'انجام شد', message: 'همه فعالیت‌ها به عنوان دیده‌شده علامت‌گذاری شدند.' })
    await refresh()
    await refreshUnseen()
  } finally {
    markAllLoading.value = false
  }
}

useHead(
  generateSeoMeta({
    title: 'تاریخچه فعالیت‌ها',
    description: 'مشاهده و مدیریت تاریخچه فعالیت‌های حساب کاربری',
    image: '',
    url: '',
    keywords: ['فعالیت', 'تاریخچه'],
    author: 'AriaSkill',
    type: 'website',
  }),
)
</script>
