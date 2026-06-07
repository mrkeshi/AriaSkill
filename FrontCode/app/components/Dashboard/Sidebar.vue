<template>
  <aside
    :class="[
      'sticky top-0 h-screen transition-all duration-300 flex flex-col',
      'backdrop-blur-xl shadow-[0_0_40px_rgba(0,0,0,0.5)] bg-slate-950/40 border-l border-white/10 relative overflow-hidden',
      collapsed ? 'w-20' : 'w-72'
    ]"
  >
    <div class="absolute -top-20 -left-20 w-40 h-40 bg-classic-gold/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-20 -right-20 w-40 h-40 bg-red-500/5 rounded-full blur-3xl pointer-events-none"></div>

    <Confirm
      v-model="logout"
      title="خروج"
      description="آیا برای خروج مطمئن هستید؟"
      @confirm="auth.logout"
    />

    <div class="flex items-center justify-between h-20 px-4 border-b border-white/10 shrink-0 relative z-10">
      <div class="flex items-center gap-2">
        <button
          class="flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 bg-white/5 text-white transition-all duration-300 hover:bg-white/10 hover:border-classic-gold/30 hover:text-classic-gold"
          @click="$emit('toggle')"
        >
          <Icon name="mdi:menu" class="text-xl" />
        </button>
      </div>

      <span v-if="!collapsed" class="text-xl font-black text-transparent bg-clip-text bg-gradient-to-l from-amber-400 via-classic-gold to-yellow-500 pl-1 drop-shadow-[0_2px_10px_rgba(212,175,55,0.4)] tracking-wider">
        SkillSphere
      </span>
    </div>

    <div class="flex-1 overflow-y-auto py-6 px-3 custom-scrollbar flex flex-col gap-1.5 relative z-10">

      <NuxtLink
        v-for="item in userMenuItems"
        :key="item.path"
        :to="item.path"
        class="group relative flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 border border-transparent text-white/60 hover:bg-white/[0.04] hover:text-white"
        :class="item.exact ? (isActiveDSH(item.path) ? 'active-link' : '') : (isActive(item.path) ? 'active-link' : '')"
      >
        <div class="absolute right-0 top-1/4 bottom-1/4 w-[3px] rounded-l-full bg-classic-gold opacity-0 transition-all duration-300 active-line"></div>

        <div class="relative shrink-0">
          <Icon :name="item.icon" class="text-xl transition-transform duration-300 group-hover:scale-110" />

          <!-- Activity badge -->
          <span
            v-if="item.path === '/dashboard/activities' && unseenCount > 0 && !collapsed"
            class="absolute -top-1.5 -left-1.5 min-w-[16px] h-4 flex items-center justify-center rounded-full bg-classic-gold text-black text-[9px] font-black px-1 leading-none"
          >
            {{ unseenCount > 99 ? '99+' : unseenCount }}
          </span>

          <!-- Notification badge -->
          <span
            v-if="item.path === '/dashboard/notifications' && unreadNotifCount > 0 && !collapsed"
            class="absolute -top-1.5 -left-1.5 min-w-[16px] h-4 flex items-center justify-center rounded-full bg-rose-500 text-white text-[9px] font-black px-1 leading-none"
          >
            {{ unreadNotifCount > 99 ? '99+' : unreadNotifCount }}
          </span>

          <!-- Collapsed dot badges -->
          <span
            v-if="item.path === '/dashboard/activities' && unseenCount > 0 && collapsed"
            class="absolute top-1 right-1 w-2 h-2 rounded-full bg-classic-gold"
          ></span>
          <span
            v-if="item.path === '/dashboard/notifications' && unreadNotifCount > 0 && collapsed"
            class="absolute top-1 right-1 w-2 h-2 rounded-full bg-rose-500"
          ></span>
        </div>

        <span v-if="!collapsed" class="truncate font-medium text-sm tracking-wide flex-1">{{ item.label }}</span>
      </NuxtLink>

      <!-- Admin section -->
      <div v-if="auth.isAdmin" class="mt-6 pt-4 border-t border-gradient flex flex-col gap-1.5">
        <p v-if="!collapsed" class="px-4 text-[10px] font-extrabold uppercase tracking-widest text-classic-gold/50 mb-2 mt-1">
          سطح دسترسی: مدیر
        </p>

        <NuxtLink
          v-for="item in adminMenuItems"
          :key="item.path"
          :to="item.path"
          class="group relative flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 border border-transparent text-white/50 hover:bg-white/[0.04] hover:text-white"
          :class="isActive(item.path) ? 'active-admin-link' : ''"
        >
          <div class="absolute right-0 top-1/4 bottom-1/4 w-[3px] rounded-l-full bg-cyan-400 opacity-0 transition-all duration-300 active-line"></div>
          <Icon :name="item.icon" class="text-xl shrink-0 transition-transform duration-300 group-hover:scale-110" />
          <span v-if="!collapsed" class="truncate font-medium text-sm tracking-wide">{{ item.label }}</span>
        </NuxtLink>
      </div>

    </div>

    <div class="p-4 border-t border-white/10 shrink-0 relative z-10">
      <button
        class="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 text-rose-400 bg-rose-500/5 hover:bg-rose-500/20 border border-rose-500/10 hover:border-rose-500/30 group shadow-[0_0_15px_rgba(244,63,94,0.02)] hover:shadow-[0_0_20px_rgba(244,63,94,0.1)]"
        @click="logout = true"
      >
        <Icon name="mdi:logout" class="text-xl shrink-0 transition-transform duration-300 group-hover:-translate-x-1" />
        <span v-if="!collapsed" class="font-bold text-sm tracking-wide">خروج از حساب</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

defineProps({ collapsed: Boolean })
const auth = useAuthStore()

const route  = useRoute()
const logout = ref(false)

// ── Activity unseen count ──────────────────────────────────────────────────
const { data: unseenData } = await useAsyncData(
  'activity-unseen-count',
  () => import('~/services/activity/activity.Service').then(m => m.getUnseenActivityCountService()),
  { server: false },
)
const unseenCount = computed(() => unseenData.value?.data?.unseen_count ?? 0)

// ── Notification unread count ──────────────────────────────────────────────
const { data: notifData } = await useAsyncData(
  'notification-unread-count',
  () => import('~/services/notification/notification.Service').then(m => m.getUnreadNotificationCountService()),
  { server: false },
)
const unreadNotifCount = computed(() => notifData.value?.data?.unread_count ?? 0)

// ── Route helpers ──────────────────────────────────────────────────────────
const isActive    = (path) => route.path.startsWith(path)
const isActiveDSH = (path) => route.path === path

// ── Menu items ─────────────────────────────────────────────────────────────
const userMenuItems = [
  { path: '/dashboard',               label: 'داشبورد',       icon: 'mdi:view-dashboard',           exact: true },
  { path: '/dashboard/projects',      label: 'پروژه‌ها',       icon: 'mdi:folder-outline' },
  { path: '/dashboard/activities',    label: 'فعالیت‌ها',      icon: 'mdi:history' },
  { path: '/dashboard/notifications', label: 'نوتیفیکیشن‌ها',  icon: 'mdi:bell-outline' },
  { path: '/dashboard/comments',      label: 'نظرات',          icon: 'mdi:comment-outline' },
  { path: '/dashboard/profile',       label: 'پروفایل',        icon: 'mdi:account-circle-outline' },
]

const adminMenuItems = [
  { path: '/dashboard/admin/users',         label: 'مدیریت کاربران',        icon: 'mdi:account-group-outline' },
  { path: '/dashboard/admin/projects',      label: 'مدیریت پروژه‌ها',        icon: 'mdi:folder-cog-outline' },
  { path: '/dashboard/admin/comments',      label: 'مدیریت نظرات',           icon: 'mdi:comment-processing-outline' },
  { path: '/dashboard/admin/skills',        label: 'مدیریت مهارت‌ها',         icon: 'mdi:tag-multiple-outline' },
  { path: '/dashboard/admin/notifications', label: 'نوتیفیکیشن‌ها (ادمین)',   icon: 'mdi:bullhorn-outline' },
]
</script>

<style scoped>
.active-link {
  background: linear-gradient(90deg, rgba(212, 175, 55, 0.02) 0%, rgba(212, 175, 55, 0.12) 100%) !important;
  color: #d4af37 !important;
  border-color: rgba(212, 175, 55, 0.2) !important;
  box-shadow: inset -10px 0 20px rgba(212, 175, 55, 0.05), 0 0 15px rgba(212, 175, 55, 0.05);
}

.active-admin-link {
  background: linear-gradient(90deg, rgba(34, 211, 238, 0.01) 0%, rgba(34, 211, 238, 0.1) 100%) !important;
  color: #22d3ee !important;
  border-color: rgba(34, 211, 238, 0.2) !important;
  box-shadow: inset -10px 0 20px rgba(34, 211, 238, 0.03);
}

.active-link .active-line, .active-admin-link .active-line {
  opacity: 1 !important;
  height: 50%;
}

.border-t-gradient {
  border-top: 1px solid transparent;
  border-image: linear-gradient(to left, rgba(255,255,255,0.1), rgba(212, 175, 55, 0.3), rgba(255,255,255,0.1)) 1;
}

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.08);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(212, 175, 55, 0.3);
}
</style>
