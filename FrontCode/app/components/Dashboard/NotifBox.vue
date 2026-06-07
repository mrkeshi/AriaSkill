<template>
  <div class="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 overflow-hidden relative select-none">

    <!-- background glows -->
    <div class="absolute -top-24 -left-24 w-48 h-48 bg-purple-500/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-24 -right-24 w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

    <!-- header -->
    <div class="flex items-center justify-between mb-8 relative z-10" dir="rtl">
      <div class="flex items-center gap-3">
        <div class="w-2 h-5 bg-gradient-to-b from-amber-400 to-classic-gold rounded-full shadow-[0_0_10px_rgba(212,175,55,0.5)]"></div>
        <h2 class="text-lg font-black text-white tracking-wide ">مرکز اعلان‌ها</h2>
        <span
          v-if="unreadCount > 0"
          class="px-2 py-0.5 rounded-full bg-rose-500/20 border border-rose-500/30 text-rose-400 text-[11px] font-bold"
        >
          {{ unreadCount }}
        </span>
      </div>
      <button
        @click="markAllRead"
        :disabled="markingAll || unreadCount === 0"
        class="text-xs font-semibold px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-classic-gold hover:text-amber-300 transition-all duration-300 flex items-center gap-1.5 disabled:opacity-40 disabled:cursor-not-allowed"
      >
        <Icon name="mdi:check-all" size="14" />
        خواندن همه
      </button>
    </div>

    <!-- skeleton -->
    <div v-if="loading" class="space-y-3 relative z-10" dir="rtl">
      <div
        v-for="i in 4"
        :key="i"
        class="h-16 rounded-xl bg-white/5 animate-pulse"
      ></div>
    </div>

    <!-- empty state -->
    <div
      v-else-if="notifications.length === 0"
      class="flex flex-col items-center justify-center py-10 text-gray-500 relative z-10"
    >
      <Icon name="mdi:bell-sleep-outline" class="text-4xl mb-3 opacity-30" />
      <p class="text-sm">هیچ اعلانی وجود ندارد.</p>
    </div>

    <!-- list -->
    <div v-else class="space-y-3 relative z-10" dir="rtl">
      <div
        v-for="notif in notifications"
        :key="notif.id"
        class="group relative flex items-center justify-between p-4 rounded-xl border transition-all duration-300 bg-slate-950/20 backdrop-blur-md"
        :class="[
          notif.is_read
            ? 'border-white/5 opacity-60'
            : 'border-white/10 hover:border-white/20 hover:bg-white/[0.04]',
          typeStyle(notif.type).borderHover,
        ]"
      >
        <!-- unread accent line -->
        <div
          v-if="!notif.is_read"
          class="absolute right-0 top-0 bottom-0 w-[3px] rounded-r-full transition-all duration-300"
          :class="typeStyle(notif.type).sideLine"
        ></div>

        <div class="flex items-center gap-4 flex-1 min-w-0">
          <div
            class="w-10 h-10 flex items-center justify-center rounded-xl border shrink-0 transition-transform duration-300 group-hover:scale-105"
            :class="typeStyle(notif.type).iconBox"
          >
            <Icon :name="typeStyle(notif.type).icon" size="18" />
          </div>

          <div class="flex flex-col gap-1 min-w-0 text-right">
            <p class="text-sm font-bold text-gray-100 group-hover:text-white transition-colors truncate">
              {{ notif.title }}
            </p>
            <p class="text-xs text-gray-400 leading-relaxed truncate pl-4">
              {{ notif.message }}
            </p>
          </div>
        </div>

        <div class="flex items-center gap-3 shrink-0 mr-4">
          <span class="text-[10px] font-medium text-gray-500 whitespace-nowrap">
            {{ relativeTime(notif.created_at) }}
          </span>

          <!-- mark read button -->
          <button
            v-if="!notif.is_read"
            @click="markRead(notif)"
            class="opacity-0 group-hover:opacity-100 text-emerald-400 hover:text-emerald-300 p-1 rounded-lg hover:bg-emerald-500/10 transition-all duration-300"
            title="علامت‌گذاری به عنوان خوانده شده"
          >
            <Icon name="mdi:check-circle-outline" size="16" />
          </button>

          <button
            @click="removeNotif(notif.id)"
            class="opacity-0 group-hover:opacity-100 text-gray-500 hover:text-rose-400 p-1 rounded-lg hover:bg-rose-500/10 transition-all duration-300"
            title="حذف اعلان"
          >
            <Icon name="mdi:delete-outline" size="16" />
          </button>
        </div>
      </div>
    </div>

    <!-- footer link -->
    <div class="mt-6 text-center relative z-10">
      <NuxtLink
        to="/dashboard/notifications"
        class="text-xs text-gray-500 hover:text-classic-gold transition-colors"
      >
        مشاهده همه اعلان‌ها ←
      </NuxtLink>
    </div>

  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import type { NotificationDTO } from '~/models/Notification/NotificationDTO'
import {
  getRecentNotificationsService,
  markNotificationReadService,
  markAllNotificationsReadService,
  deleteNotificationService,
} from '~/services/notification/notification.Service'

// ── State ──────────────────────────────────────────────────────────────────
const notifications = ref<NotificationDTO[]>([])
const loading      = ref(true)
const markingAll   = ref(false)

const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length)

// ── Type styling ───────────────────────────────────────────────────────────
const typeStyle = (type: string) => {
  const map: Record<string, { iconBox: string; sideLine: string; borderHover: string; icon: string }> = {
    login_failed: {
      iconBox: 'border-rose-500/40 bg-rose-500/10 text-rose-400 shadow-[0_0_15px_rgba(244,63,94,0.15)]',
      sideLine: 'bg-rose-500',
      borderHover: 'hover:border-rose-500/30',
      icon: 'mdi:shield-alert-outline',
    },
    comment_created: {
      iconBox: 'border-cyan-500/30 bg-cyan-500/10 text-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.1)]',
      sideLine: 'bg-cyan-500',
      borderHover: 'hover:border-cyan-500/30',
      icon: 'mdi:comment-outline',
    },
    like_received: {
      iconBox: 'border-amber-500/30 bg-amber-500/10 text-classic-gold shadow-[0_0_15px_rgba(212,175,55,0.1)]',
      sideLine: 'bg-classic-gold',
      borderHover: 'hover:border-classic-gold/30',
      icon: 'mdi:heart-outline',
    },
    broadcast: {
      iconBox: 'border-purple-500/30 bg-purple-500/10 text-purple-400 shadow-[0_0_15px_rgba(168,85,247,0.1)]',
      sideLine: 'bg-purple-500',
      borderHover: 'hover:border-purple-500/30',
      icon: 'mdi:bullhorn-outline',
    },
  }
  return map[type] ?? {
    iconBox: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400',
    sideLine: 'bg-emerald-500',
    borderHover: 'hover:border-emerald-500/30',
    icon: 'mdi:bell-outline',
  }
}

// ── Time helper ────────────────────────────────────────────────────────────
const relativeTime = (iso: string) => {
  const diff = Date.now() - new Date(iso).getTime()
  const mins  = Math.floor(diff / 60000)
  const hours = Math.floor(mins / 60)
  const days  = Math.floor(hours / 24)
  if (mins < 1)   return 'لحظاتی پیش'
  if (mins < 60)  return `${mins} دقیقه پیش`
  if (hours < 24) return `${hours} ساعت پیش`
  if (days === 1) return 'دیروز'
  return `${days} روز پیش`
}

// ── Fetch ──────────────────────────────────────────────────────────────────
const fetchNotifications = async () => {
  loading.value = true
  try {
    const res = await getRecentNotificationsService()
    notifications.value = res?.data ?? res ?? []
  } catch {
    notifications.value = []
  } finally {
    loading.value = false
  }
}

// ── Actions ────────────────────────────────────────────────────────────────
const markRead = async (notif: NotificationDTO) => {
  try {
    await markNotificationReadService(notif.id)
    notif.is_read = true
  } catch { /* silent */ }
}

const markAllRead = async () => {
  markingAll.value = true
  try {
    await markAllNotificationsReadService()
    notifications.value.forEach(n => (n.is_read = true))
  } catch { /* silent */ }
  finally { markingAll.value = false }
}

const removeNotif = async (id: number) => {
  try {
    await deleteNotificationService(id)
    notifications.value = notifications.value.filter(n => n.id !== id)
  } catch { /* silent */ }
}

onMounted(fetchNotifications)
</script>

<style scoped>
.from-classic-gold {
  --tw-gradient-from: #d4af37 var(--tw-gradient-from-position);
  --tw-gradient-to: rgb(212 175 55 / 0) var(--tw-gradient-to-position);
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to);
}
.to-classic-gold {
  --tw-gradient-to: #d4af37 var(--tw-gradient-to-position);
}
</style>
