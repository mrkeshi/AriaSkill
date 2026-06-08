<template>
  <div class="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 mt-6 overflow-hidden relative select-none">

    <div class="absolute -top-24 -right-24 w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-24 -left-24 w-48 h-48 bg-purple-500/10 rounded-full blur-3xl pointer-events-none"></div>

    <div class="flex items-center justify-between mb-5 relative z-10" dir="rtl">
      <div class="flex items-center gap-3">
        <div class="w-2 h-5 bg-gradient-to-b from-amber-400 to-classic-gold rounded-full shadow-[0_0_10px_rgba(212,175,55,0.5)]"></div>
        <h3 class="text-base font-black text-white tracking-wide">مرور فعالیت‌های اخیر</h3>
      </div>
      <NuxtLink
        to="/dashboard/activities"
        class="flex items-center gap-1.5 text-xs text-gray-400 hover:text-classic-gold border border-white/10 hover:border-classic-gold/30 px-3 py-1.5 rounded-lg transition-all duration-200"
      >
        <span>مشاهده همه</span>
        <Icon name="mdi:chevron-left" size="14" />
      </NuxtLink>
    </div>

    <SkeletonSimple v-if="pending" :repeat="6" class="h-20 mb-3" />

    <div v-else-if="activities.length === 0" class="relative z-10 flex flex-col items-center justify-center py-10 text-gray-500 gap-2" dir="rtl">
      <Icon name="mdi:history" class="text-4xl text-gray-600" />
      <span class="text-sm">هنوز فعالیتی ثبت نشده است.</span>
    </div>

    <div v-else class="relative z-10 grid grid-cols-1 md:grid-cols-2 gap-3" dir="rtl">
      <div
        v-for="activity in activities"
        :key="activity.id"
        class="group relative bg-slate-950/20 hover:bg-white/[0.03] border border-white/5 hover:border-white/10 rounded-xl p-4 flex items-start gap-3.5 transition-all duration-300 transform hover:-translate-y-0.5"
        :class="{ 'opacity-60': activity.is_seen }"
      >
        <div
          class="absolute right-0 top-3 bottom-3 w-[2.5px] rounded-l-full opacity-60 group-hover:opacity-100 transition-opacity"
          :class="activityStyle(activity.type).line"
        ></div>

        <div
          class="w-9 h-9 flex items-center justify-center rounded-lg border shrink-0 transition-all duration-500 group-hover:scale-105"
          :class="activityStyle(activity.type).iconContainer"
        >
          <Icon :name="activityStyle(activity.type).icon" size="16" />
        </div>

        <div class="flex flex-col justify-between flex-1 min-w-0 h-full gap-2 text-right">
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <h4 class="text-xs font-bold text-gray-200 group-hover:text-white transition-colors truncate">
                {{ activity.title }}
              </h4>
              <span
                class="text-[9px] px-1.5 py-0.5 rounded font-bold whitespace-nowrap border"
                :class="activityStyle(activity.type).badge"
              >
                {{ activityStyle(activity.type).label }}
              </span>
              <span v-if="!activity.is_seen" class="w-1.5 h-1.5 rounded-full bg-classic-gold shrink-0"></span>
            </div>
            <p class="text-[11px] text-gray-400 leading-relaxed mt-1 line-clamp-2 pl-2">
              {{ activity.description }}
            </p>
          </div>

          <div class="flex items-center justify-between pt-1.5 border-t border-white/[0.03]">
            <div class="flex items-center gap-1 text-gray-500 text-[10px] font-medium">
              <Icon name="mdi:clock-outline" size="12" />
              <span>{{ toJalaliWithTime(activity.created_at) }}</span>
            </div>
            <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                v-if="!activity.is_seen"
                type="button"
                class="p-1 rounded-md bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/30 transition-colors"
                :disabled="loadingId === activity.id"
                @click.stop="handleMarkSeen(activity)"
              >
                <Icon name="mdi:check" size="11" />
              </button>
              <button
                type="button"
                class="p-1 rounded-md bg-rose-500/20 text-rose-400 border border-rose-500/30 hover:bg-rose-500/30 transition-colors"
                :disabled="loadingId === activity.id"
                @click.stop="openDelete(activity.id)"
              >
                <Icon name="mdi:trash-can-outline" size="11" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Confirm
      v-model="deleteModal"
      title="حذف فعالیت"
      description="آیا مطمئن هستید که می‌خواهید این فعالیت را حذف کنید؟"
      @confirm="handleDelete"
    />
  </div>
</template>

<script setup lang="ts">
/**
 * - Renders a sleek asynchronous log dashboard widget mapping recent profile operations.
 * - Eradicates possible compile-time 'undefined' breakages using runtime short-circuiting (?.).
 * - Orchestrates reactive data hydration pipelines natively coupled with global layout listeners.
 */
import type { ActivityDTO, ActivityType } from '~/models/Activity/ActivityDTO'
import {
  deleteActivityService,
  getRecentActivitiesService,
  markActivitySeenService,
} from '~/services/activity/activity.Service'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { toJalaliWithTime } from '~/utilities/dateHelpers'
import { activityStyle } from '~/utilities/activityHelpers'
import { useDeleteModal } from '~/composable/useDeleteModal'

const { showInfo } = useCustomToastify()
const { deleteModal, selectedItem: selectedId, openDelete } = useDeleteModal<number>()
const loadingId = ref<number | null>(null)

const { data, pending, refresh } = await useAsyncData(
  'recent-activities',
  () => getRecentActivitiesService(),
)

const activities = computed<ActivityDTO[]>(() => data.value?.data ?? [])

const handleMarkSeen = async (activity: ActivityDTO) => {
  loadingId.value = activity.id
  try {
    await markActivitySeenService(activity.id, true)
    activity.is_seen = true
    await refreshNuxtData('activity-unseen-count')
  } finally {
    loadingId.value = null
  }
}

const handleDelete = async () => {
  if (!selectedId.value) return
  try {
    await deleteActivityService(selectedId.value)
    showInfo({ title: 'فعالیت حذف شد', message: 'فعالیت با موفقیت حذف شد.' })
    await refresh()
    await refreshNuxtData('activity-unseen-count')
  } finally {
    selectedId.value = null
  }
}
</script>
