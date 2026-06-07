<template>
  <div class="space-y-6 select-none" dir="rtl">

    <div class="flex items-start gap-3">
      <div class="w-1.5 h-8 bg-gradient-to-b from-cyan-400 to-classic-gold rounded-full shadow-[0_0_12px_rgba(6,182,212,0.4)] mt-1"></div>
      <div>
        <h1 class="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-l from-white via-gray-100 to-gray-300 tracking-wide">
          پیشخوان سیستم
        </h1>
        <p class="text-xs text-gray-400 mt-1">مرور کلی و خلاصه فعالیت‌های جاری معماری پلتفرم شما</p>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6" dir="rtl">
      <div
        v-for="stat in stats"
        :key="stat.id"
        class="group relative bg-white/[0.02] backdrop-blur-xl border border-white/10 rounded-2xl p-5 flex items-center gap-5 transition-all duration-500 hover:-translate-y-1.5 hover:bg-white/[0.04] overflow-hidden"
        :class="stat.shadowColor"
      >
        <!-- glow blob -->
        <div
          class="absolute -right-10 -bottom-10 w-28 h-28 rounded-full blur-3xl opacity-20 group-hover:opacity-40 transition-opacity duration-500 pointer-events-none"
          :class="stat.bgGlow"
        ></div>

        <!-- icon -->
        <div
          class="flex items-center justify-center w-14 h-14 rounded-2xl border transition-all duration-500 group-hover:scale-110"
          :class="stat.iconStyle"
        >
          <Icon :name="stat.icon" size="28" />
        </div>

        <!-- value + label -->
        <div class="flex flex-col gap-1 flex-1 min-w-0 text-right">

          <!-- skeleton while loading -->
          <div v-if="loading" class="h-7 w-16 bg-white/10 rounded-lg animate-pulse mb-1"></div>
          <p v-else class="text-2xl font-black text-white tracking-wider ">
            {{ toPersianNumerals(stat.value) }}
          </p>

          <p class="text-xs font-medium text-gray-400 group-hover:text-gray-300 transition-colors">
            {{ stat.label }}
          </p>
        </div>

        <!-- accent line -->
        <div
          class="absolute right-0 top-1/4 bottom-1/4 w-[2px] rounded-r-full opacity-40 group-hover:opacity-100 transition-opacity duration-500"
          :class="stat.lineStyle"
        ></div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDashboardStatsService } from '~/services/notification/notification.Service'

// ── Persian numeral helper ─────────────────────────────────────────────────
const toPersianNumerals = (n: number) =>
  n.toLocaleString('fa-IR')

// ── Reactive state ─────────────────────────────────────────────────────────
const loading = ref(true)

interface StatCard {
  id: number
  label: string
  value: number
  icon: string
  iconStyle: string
  shadowColor: string
  bgGlow: string
  lineStyle: string
}

const stats = ref<StatCard[]>([
  {
    id: 1,
    label: 'پروژه‌های توسعه‌یافته',
    value: 0,
    icon: 'mdi:folder-outline',
    iconStyle: 'bg-cyan-500/10 border-cyan-500/20 text-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.1)] group-hover:shadow-[0_0_25px_rgba(6,182,212,0.3)]',
    shadowColor: 'hover:shadow-[0_10px_30px_rgba(6,182,212,0.08)] hover:border-cyan-500/20',
    bgGlow: 'bg-cyan-500',
    lineStyle: 'bg-cyan-400',
  },
  {
    id: 2,
    label: 'کل دانلودهای ثبت‌شده',
    value: 0,
    icon: 'mdi:download-outline',
    iconStyle: 'bg-purple-500/10 border-purple-500/20 text-purple-400 shadow-[0_0_15px_rgba(168,85,247,0.1)] group-hover:shadow-[0_0_25px_rgba(168,85,247,0.3)]',
    shadowColor: 'hover:shadow-[0_10px_30px_rgba(168,85,247,0.08)] hover:border-purple-500/20',
    bgGlow: 'bg-purple-500',
    lineStyle: 'bg-purple-400',
  },
  {
    id: 3,
    label: 'نظرات و بازخوردها',
    value: 0,
    icon: 'mdi:comment-outline',
    iconStyle: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.1)] group-hover:shadow-[0_0_25px_rgba(16,185,129,0.3)]',
    shadowColor: 'hover:shadow-[0_10px_30px_rgba(16,185,129,0.08)] hover:border-emerald-500/20',
    bgGlow: 'bg-emerald-500',
    lineStyle: 'bg-emerald-400',
  },
  {
    id: 4,
    label: 'اعلان‌های خوانده‌نشده',
    value: 0,
    icon: 'mdi:bell-outline',
    iconStyle: 'bg-amber-500/10 border-amber-500/20 text-classic-gold shadow-[0_0_15px_rgba(212,175,55,0.1)] group-hover:shadow-[0_0_25px_rgba(212,175,55,0.3)]',
    shadowColor: 'hover:shadow-[0_10px_30px_rgba(212,175,55,0.08)] hover:border-amber-500/20',
    bgGlow: 'bg-amber-500',
    lineStyle: 'bg-classic-gold',
  },
])

// ── Fetch stats ────────────────────────────────────────────────────────────
const fetchStats = async () => {
  loading.value = true
  try {
    const res = await getDashboardStatsService()
    const data = res?.data ?? res
    stats.value[0].value = data.total_projects      ?? 0
    stats.value[1].value = data.total_downloads     ?? 0
    stats.value[2].value = data.total_comments      ?? 0
    stats.value[3].value = data.unread_notifications ?? 0
  } catch {
    // اگر API خطا داد مقادیر 0 نمایش داده می‌شه
  } finally {
    loading.value = false
  }
}

onMounted(fetchStats)
</script>
