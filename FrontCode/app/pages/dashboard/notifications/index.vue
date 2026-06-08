<template>
  <UiCardBlury>

    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-5 gap-3">
      <h2 class="text-base font-bold text-white tracking-wide">اعلان‌ها</h2>

      <!-- Tabs -->
      <div class="flex p-0.5 bg-black/30 rounded-lg border border-white/10 backdrop-blur-sm">
        <button
          @click="setTab('unread')"
          :class="[
            'px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200',
            activeTab === 'unread'
              ? 'bg-white/15 text-white shadow-lg'
              : 'text-gray-400 hover:text-gray-200',
          ]"
        >
          نخوانده شده
          <span
            v-if="unreadCount > 0"
            class="mr-1.5 px-1.5 py-0.5 rounded-full bg-indigo-500 text-white text-[11px] font-bold"
          >
            {{ unreadCount }}
          </span>
        </button>

        <button
          @click="setTab('read')"
          :class="[
            'px-4 py-1.5 rounded-md text-sm font-medium transition-all duration-200',
            activeTab === 'read'
              ? 'bg-white/15 text-white shadow-lg'
              : 'text-gray-400 hover:text-gray-200',
          ]"
        >
          خوانده شده
        </button>
      </div>
    </div>

    <!-- Type filter bar -->
    <div class="flex flex-wrap gap-2 mb-5" dir="rtl">
      <button
        v-for="f in filterOptions"
        :key="f.value"
        @click="setTypeFilter(f.value)"
        :class="[
          'flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border transition-all duration-200',
          typeFilter === f.value
            ? 'bg-white/15 border-white/20 text-white'
            : 'bg-white/5 border-white/10 text-gray-400 hover:text-gray-200 hover:border-white/20',
        ]"
      >
        <Icon :name="f.icon" size="13" />
        {{ f.label }}
      </button>
    </div>

    <!-- Mark-all button row -->
    <div v-if="activeTab === 'unread' && unreadCount > 0" class="flex justify-end mb-4">
      <button
        @click="markAllRead"
        :disabled="markingAll"
        class="flex items-center gap-2 text-xs text-emerald-400 hover:text-emerald-300 border border-emerald-500/30 bg-emerald-500/10 hover:bg-emerald-500/20 px-4 py-1.5 rounded-lg transition-all disabled:opacity-50"
      >
        <Icon name="mdi:check-all" size="14" />
        {{ markingAll ? 'در حال اجرا...' : 'علامت‌گذاری همه به عنوان خوانده شده' }}
      </button>
    </div>

    <!-- Skeleton loader -->
    <div v-if="loading" class="flex flex-col gap-2">
      <div v-for="i in 5" :key="i" class="h-14 rounded-lg bg-white/5 animate-pulse"></div>
    </div>


    <div
      v-else-if="items.length === 0"
      class="flex flex-col items-center justify-center py-10 text-gray-500"
    >
      <Icon name="mdi:bell-sleep-outline" class="text-4xl mb-3 opacity-30" />
      <p class="text-sm">هیچ اعلانی در این بخش وجود ندارد.</p>
    </div>

    <div v-else class="flex flex-col gap-2">
      <div
        v-for="item in items"
        :key="item.id"
        class="group flex items-center gap-2.5 p-2.5 rounded-lg border transition-all duration-200 backdrop-blur-md hover:scale-[1.01]"
        :class="[
          item.is_read
            ? 'bg-white/5 border-white/5 opacity-50 hover:opacity-80'
            : 'bg-gradient-to-r from-white/10 to-white/5 border-white/10 hover:border-white/20 shadow-md',
        ]"
      >
        <!-- type icon -->
        <div
          class="shrink-0 flex items-center justify-center w-9 h-9 rounded-lg border"
          :class="notifStyle(item.type).iconBox"
        >
          <Icon :name="notifStyle(item.type).icon" class="text-lg" />
        </div>

        <div class="flex-grow min-w-0">
          <div class="flex items-center justify-between gap-2 mb-0.5">
            <h3 class="text-sm text-gray-100 font-semibold truncate">{{ item.title }}</h3>
            <span class="text-[11px] text-gray-500 whitespace-nowrap">
              {{ relativeTime(item.created_at) }}
            </span>
          </div>
          <p class="text-[12px] text-gray-400 leading-relaxed line-clamp-1">{{ item.message }}</p>
        </div>

        <!-- Actions -->
        <div class="shrink-0 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <button
            v-if="!item.is_read"
            @click="markRead(item)"
            title="علامت‌گذاری به عنوان خوانده شده"
            class="p-1.5 rounded-md bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/30 transition-colors"
          >
            <Icon name="mdi:check-all" class="text-sm" />
          </button>

          <button
            @click="removeItem(item.id)"
            title="حذف"
            class="p-1.5 rounded-md bg-rose-500/20 text-rose-400 border border-rose-500/30 hover:bg-rose-500/30 transition-colors"
          >
            <Icon name="mdi:trash-can-outline" class="text-sm" />
          </button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-center gap-3 mt-6">
      <button
        :disabled="page <= 1"
        @click="changePage(page - 1)"
        class="px-3 py-1.5 rounded-lg text-sm border border-white/10 bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 transition disabled:opacity-30 disabled:cursor-not-allowed"
      >
        قبلی
      </button>
      <span class="text-sm text-gray-400">
        صفحه {{ page }} از {{ totalPages }}
      </span>
      <button
        :disabled="page >= totalPages"
        @click="changePage(page + 1)"
        class="px-3 py-1.5 rounded-lg text-sm border border-white/10 bg-white/5 text-gray-400 hover:text-white hover:bg-white/10 transition disabled:opacity-30 disabled:cursor-not-allowed"
      >
        بعدی
      </button>
    </div>

  </UiCardBlury>
</template>

<script setup>
/**
 * @page AdminNotificationCenterLog
 * @description Advanced back-office notification auditing log featuring multi-tiered criteria filtering.
 * Bridges asynchronous rest streams directly with reactive pinia global navigation badge handlers.
 * 
 * @logic_flow
 * - Dynamic Filtering: Cascades combined watcher matrices (`activeTab`, `typeFilter`, `page`) into standard unified resource requests.
 * - Tab State Mutations: Enforces implicit routing resets (`page.value = 1`) upon toggle transitions to eliminate layout truncation.
 * - Reactive Interception: Manages conditional component slicing within `markRead` routines to prune visual nodes locally on success.
 * 
 * @store_synchronization
 * - Pinia Bridge: Triggers manual internal decrements (`notifStore.decrement`) and global flushes (`notifStore.reset`) 
 *   to ensure header layout indicators map exactly to the updated transactional log states.
 * 
 * @author Alireza Keshavarz
 */
import { ref, computed, watch, onMounted } from 'vue'
import { generateSeoMeta } from '~/utilities/seo'
import {
  getNotificationsService,
  markNotificationReadService,
  markAllNotificationsReadService,
  deleteNotificationService,
} from '~/services/notification/notification.Service'
import { notifStyle } from '~/utilities/notificationHelpers'
import { relativeTime } from '~/utilities/dateHelpers'

const notifStore = useNotificationStore()

definePageMeta({ layout: 'dashboard' })

const seo = generateSeoMeta({
  title: 'مدیریت نوتیفیکیشن‌ها',
  description: 'مشاهده و مدیریت اعلان‌های سیستم',
  image: '',
  url: '',
  keywords: ['نوتیفیکیشن', 'اعلان'],
  author: 'علیرضا کشاورز',
  type: 'website',
})
useHead(seo)

const activeTab  = ref('unread')
const typeFilter = ref('')
const loading    = ref(true)
const markingAll = ref(false)
const page       = ref(1)
const total      = ref(0)
const PAGE_SIZE  = 10
const items      = ref([])

const unreadCount = computed(() => {
  if (activeTab.value === 'unread') return total.value
  return 0
})

const totalPages = computed(() => Math.ceil(total.value / PAGE_SIZE))

// ── Filter options ─────────────────────────────────────────────────────────
const filterOptions = [
  { value: '',               label: 'همه',         icon: 'mdi:filter-outline' },
  { value: 'login_failed',   label: 'ورود ناموفق',  icon: 'mdi:shield-alert-outline' },
  { value: 'comment_created',label: 'نظر جدید',    icon: 'mdi:comment-outline' },
  { value: 'like_received',  label: 'لایک',         icon: 'mdi:heart-outline' },
  { value: 'broadcast',      label: 'پیام همگانی', icon: 'mdi:bullhorn-outline' },
]

// ── Fetch ──────────────────────────────────────────────────────────────────
const fetchItems = async () => {
  loading.value = true
  try {
    const isRead   = activeTab.value === 'read'
    const typeVal  = typeFilter.value || undefined
    const res = await getNotificationsService(page.value, typeVal, isRead)
    const data = res?.data ?? res
    items.value = data?.results ?? []
    total.value = data?.count   ?? 0
  } catch {
    items.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// ── Watchers & navigation ──────────────────────────────────────────────────
const setTab = (tab) => {
  activeTab.value = tab
  page.value = 1
}

const setTypeFilter = (val) => {
  typeFilter.value = val
  page.value = 1
}

const changePage = (p) => { page.value = p }

watch([activeTab, typeFilter, page], fetchItems)
onMounted(fetchItems)

// ── Actions ────────────────────────────────────────────────────────────────
const markRead = async (item) => {
  try {
    await markNotificationReadService(item.id)
    item.is_read = true
    if (activeTab.value === 'unread') {
      items.value = items.value.filter(n => n.id !== item.id)
      total.value = Math.max(0, total.value - 1)
      notifStore.decrement(1)
    }
  } catch { /* silent */ }
}

const markAllRead = async () => {
  markingAll.value = true
  try {
    await markAllNotificationsReadService()
    items.value = []
    total.value = 0
    notifStore.reset()
  } catch { /* silent */ }
  finally { markingAll.value = false }
}

const removeItem = async (id) => {
  try {
    await deleteNotificationService(id)
    items.value = items.value.filter(n => n.id !== id)
    total.value = Math.max(0, total.value - 1)
  } catch { /* silent */ }
}
</script>
