<template>
  <div class="relative" v-click-outside="closeDropdown">
    <button
      @click="toggleOpen"
      class="relative p-2.5 text-bone-white cursor-pointer hover:text-light-gold rounded-xl hover:bg-white/[0.03] transition-all duration-300"
      aria-label="Notifications"
    >
      <Icon name="mdi:bell-outline" class="text-2xl" />
      <span
        v-if="unreadCount > 0"
        class="absolute top-1.5 right-1.5 min-w-[18px] h-[18px] flex items-center justify-center rounded-full border-2 bg-rose-500 border-carb-gray text-[10px] font-bold text-white animate-pulse shadow-[0_0_10px_rgba(239,68,68,0.5)]"
      >
        {{ unreadCount > 9 ? '9+' : unreadCount }}
      </span>
    </button>

    <Transition name="glass-dropdown">
      <div
        v-if="isOpen"
        class="absolute max-md:-left-20 left-0 mt-3 w-80 border border-white/10 rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.6)] z-50 overflow-hidden backdrop-blur-xl bg-carb-gray"
      >
        <div class="p-4 border-b border-white/5 flex items-center justify-between">
          <p class="font-bold tracking-wide text-classic-gold text-sm text-center">مرکز اعلان‌های هوشمند</p>
          <button
            v-if="unreadCount > 0"
            @click="markAllRead"
            class="text-[11px] text-gray-400 hover:text-emerald-400 transition-colors flex items-center gap-1"
          >
            <Icon name="mdi:check-all" size="13" />
            خواندن همه
          </button>
        </div>

        <div v-if="loading" class="flex flex-col">
          <div v-for="i in 3" :key="i" class="px-5 py-4 border-b border-white/5 last:border-none">
            <div class="flex gap-3">
              <div class="w-6 h-6 rounded-full bg-white/10 animate-pulse shrink-0 mt-0.5"></div>
              <div class="flex-1 space-y-2">
                <div class="h-3 bg-white/10 rounded animate-pulse w-3/4"></div>
                <div class="h-2.5 bg-white/5 rounded animate-pulse w-full"></div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="!notifications || notifications.length === 0" class="py-8 text-center">
          <Icon name="mdi:bell-sleep-outline" class="text-3xl text-gray-600 mb-2" />
          <p class="text-xs text-gray-500">اعلانی وجود ندارد.</p>
        </div>

        <ul v-else class="flex flex-col max-h-72 overflow-y-auto">
          <li
            v-for="notif in notifications"
            :key="notif?.id"
            @click="handleClick(notif)"
            class="px-5 py-4 hover:bg-black/40 transition-colors duration-300 cursor-pointer border-b border-white/5 last:border-none"
            :class="notif?.is_read ? 'opacity-60' : ''"
          >
            <div class="flex items-start gap-3.5">
              <span
                v-if="!notif?.is_read"
                class="w-1.5 h-1.5 rounded-full bg-rose-500 mt-2 shrink-0"
              ></span>
              <Icon
                :name="notifIcon(notif?.type)"
                class="text-xl flex-shrink-0 mt-0.5"
                :class="notifIconColor(notif?.type)"
              />
              <div class="space-y-1 text-right flex-1 min-w-0">
                <p class="text-bone-white font-bold text-sm truncate">{{ notif?.title }}</p>
                <p class="text-xs text-gray-400 leading-relaxed line-clamp-2">{{ notif?.message }}</p>
                <p class="text-[11px] text-gray-600">{{ relativeTime(notif?.created_at) }}</p>
              </div>
            </div>
          </li>
        </ul>

        <div class="p-3 text-center border-t border-white/5 bg-black/20">
          <NuxtLink
            to="/dashboard/notifications"
            @click="closeDropdown"
            class="text-gray-500 hover:text-light-gold font-medium text-xs tracking-wide cursor-pointer transition-colors"
          >
            مشاهده آرشیو تمام اعلان‌ها
          </NuxtLink>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
/**
 * - Compact glassmorphic top-bar notification dropdown widget layout.
 * - Implements custom click-outside directives isolating layout state triggers.
 * - Utilizes defensive mathematical constraints safely capping reactive count reductions.
 */

import { ref, onMounted } from 'vue'
import type { NotificationDTO } from '~/models/Notification/NotificationDTO'
import {
  getRecentNotificationsService,
  getUnreadNotificationCountService,
  markNotificationReadService,
  markAllNotificationsReadService,
} from '~/services/notification/notification.Service'
import { notifIcon, notifIconColor } from '~/utilities/notificationHelpers'
import { relativeTime } from '~/utilities/dateHelpers'

// ── State ──────────────────────────────────────────────────────────────────
const isOpen        = ref(false)
const loading       = ref(false)
const notifications = ref<NotificationDTO[]>([])
const unreadCount   = ref(0)

// ── Data fetching ──────────────────────────────────────────────────────────
const fetchAll = async () => {
  loading.value = true
  try {
    const [notifRes, countRes] = await Promise.all([
      getRecentNotificationsService(),
      getUnreadNotificationCountService(),
    ])
    notifications.value = notifRes?.data ?? notifRes ?? []
    unreadCount.value   = (countRes?.data ?? countRes)?.unread_count ?? 0
  } catch {
    notifications.value = []
    unreadCount.value   = 0
  } finally {
    loading.value = false
  }
}

const toggleOpen = async () => {
  isOpen.value = !isOpen.value
  if (isOpen.value && (!notifications.value || notifications.value.length === 0)) {
    await fetchAll()
  }
}

const closeDropdown = () => { isOpen.value = false }

const handleClick = async (notif: NotificationDTO) => {
  if (!notif?.id) return
  if (!notif.is_read) {
    notif.is_read = true
    unreadCount.value = Math.max(0, unreadCount.value - 1)
    await markNotificationReadService(notif.id).catch(() => {})
  }
}

const markAllRead = async () => {
  try {
    await markAllNotificationsReadService()
    notifications.value?.forEach(n => {
      if (n) n.is_read = true
    })
    unreadCount.value = 0
  } catch { /* silent */ }
}

const vClickOutside = {
  mounted(el: any, binding: any) {
    el.clickOutsideEvent = (event: Event) => {
      if (!(el === event.target || el.contains(event.target))) binding.value(event)
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el: any) {
    document.removeEventListener('click', el.clickOutsideEvent)
  },
}

onMounted(async () => {
  try {
    const res = await getUnreadNotificationCountService()
    unreadCount.value = (res?.data ?? res)?.unread_count ?? 0
  } catch { /* silent */ }
})
</script>

<style scoped>
.glass-dropdown-enter-active,
.glass-dropdown-leave-active { transition: all 0.3s ease; }
.glass-dropdown-enter-from,
.glass-dropdown-leave-to { opacity: 0; transform: translateY(-10px); }
</style>