VUE
<template>
  <UiCardBlury class="lg:col-span-2 glass-box overflow-hidden relative group">
    <div class="absolute -top-20 -right-20 w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none transition-all duration-500 group-hover:bg-cyan-500/15"></div>
    <div class="absolute -bottom-20 -left-20 w-48 h-48 bg-amber-500/5 rounded-full blur-3xl pointer-events-none transition-all duration-500 group-hover:bg-amber-500/10"></div>
 
    <div class="p-6 relative z-10">
 
      <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-8 gap-4" dir="rtl">
        <div class="flex items-start gap-3">
          <div class="w-1.5 h-6 bg-gradient-to-b from-cyan-400 to-classic-gold rounded-full shadow-[0_0_12px_rgba(6,182,212,0.4)] mt-1"></div>
          <div>
            <h2 class="text-lg font-black text-transparent bg-clip-text bg-gradient-to-l from-white via-gray-100 to-gray-300 tracking-wide">
              تحلیل رفتار مخاطبان
            </h2>
            <p class="text-xs text-gray-400 mt-1.5 leading-relaxed">
              روند تجمعی {{ toPersianNumerals(chartDays) }} روز اخیر تعامل با کل پروژه‌ها
            </p>
          </div>
        </div>
 
        <div class="flex gap-5 text-xs font-semibold bg-white/[0.02] border border-white/5 px-4 py-2 rounded-xl backdrop-blur-sm self-start sm:self-auto">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-[0_0_10px_rgba(0,242,254,0.6)]"></span>
            <span class="text-gray-300">میزان بازدید</span>
          </div>
          <div class="flex items-center gap-2 border-r border-white/10 pr-5">
            <span class="w-2.5 h-2.5 rounded-full bg-[#d4af37] shadow-[0_0_10px_rgba(212,175,55,0.6)]"></span>
            <span class="text-gray-300">میزان دانلود</span>
          </div>
        </div>
      </div>
 
      <!-- Loading State -->
      <div v-if="pending" class="w-full h-[500px] flex flex-col items-center justify-center gap-3 text-gray-500 text-sm">
        <Icon name="line-md:loading-twotone-loop" size="24" class="text-classic-gold" />
        <span>در حال آنالیز و رندر داده‌ها...</span>
      </div>
 
      <!-- Empty State: No Projects -->
      <div v-else-if="isEmpty" class="w-full h-[500px] flex flex-col items-center justify-center gap-4 text-gray-500">
        <div class="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center">
          <Icon name="ph:chart-line-up-duotone" size="32" class="text-classic-gold opacity-60" />
        </div>
        <div class="text-center" dir="rtl">
          <p class="text-gray-300 font-semibold text-sm">هنوز پروژه‌ای ثبت نشده</p>
          <p class="text-gray-500 text-xs mt-1">پس از افزودن پروژه، آمار تعاملات اینجا نمایش داده می‌شود</p>
        </div>
      </div>
 
      <!-- Chart -->
      <!-- DashboardApexWrapper is a .client.vue component, so Nuxt skips it   -->
      <!-- on the server entirely — no SSR "failed to resolve apexchart" warn. -->
      <div v-else class="w-full h-[500px] text-black" dir="ltr">
        <ClientOnly>
          <DashboardApexWrapper
            width="100%"
            height="100%"
            type="area"
            :options="chartOptions"
            :series="series"
          />
          <template #fallback>
            <div class="w-full h-full flex flex-col items-center justify-center gap-3 text-gray-500 text-sm">
              <Icon name="line-md:loading-twotone-loop" size="24" class="text-classic-gold" />
              <span>در حال رندر نمودار...</span>
            </div>
          </template>
        </ClientOnly>
      </div>
 
    </div>
  </UiCardBlury>
</template>
 
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getDashboardChartService } from '~/services/projects/chart.Service'
import { toPersianNumerals, toJalali } from '~/utilities/dateHelpers'
 
// ── State ──────────────────────────────────────────────────────────────────
const pending = ref(true)
const isEmpty = ref(false)
 
const rawDays    = ref<string[]>([])
const rawViews   = ref<number[]>([])
const rawDownloads = ref<number[]>([])
 
// ── Computed ───────────────────────────────────────────────────────────────
const chartDays = computed(() => rawDays.value.length)
 
/** Convert ISO date string like "2026-05-20" to a Jalali short label */
const toJalaliShort = (iso: string): string => {
  try {
    const d = new Date(iso)
    const parts = new Intl.DateTimeFormat('fa-IR', {
      calendar: 'persian',
      numberingSystem: 'latn',
      month: 'numeric',
      day: 'numeric',
    }).formatToParts(d)
    const get = (type: string) => parts.find(p => p.type === type)?.value ?? ''
    const day = get('day')
    const month = get('month')
    return toPersianNumerals(`${month}/${day}`)
  } catch {
    return iso
  }
}
 
const xCategories = computed(() => rawDays.value.map(toJalaliShort))
 
const series = computed(() => [
  { name: 'بازدید',  data: rawViews.value },
  { name: 'دانلود', data: rawDownloads.value },
])
 
const chartOptions = computed(() => ({
  chart: {
    type: 'area',
    fontFamily: 'inherit',
    toolbar: { show: false },
    background: 'transparent',
    zoom: { enabled: false },
    sparkline: { enabled: false },
  },
  colors: ['#00f2fe', '#d4af37'],
  dataLabels: { enabled: false },
  stroke: {
    curve: 'smooth',
    width: 3,
    lineCap: 'round',
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      type: 'vertical',
      opacityFrom: 0.25,
      opacityTo: 0.01,
      stops: [0, 100],
    },
  },
  markers: {
    size: 0,
    colors: ['#00f2fe', '#d4af37'],
    strokeColors: '#0f172a',
    strokeWidth: 2,
    hover: { size: 6 },
  },
  xaxis: {
    categories: xCategories.value,
    axisBorder: { show: false },
    axisTicks: { show: false },
    labels: {
      style: {
        colors: '#64748b',
        fontSize: '11px',
        fontWeight: 500,
      },
    },
  },
  yaxis: {
    min: 0,
    tickAmount: 4,
    labels: {
      style: {
        colors: '#64748b',
        fontSize: '11px',
      },
      formatter: (val: number) => toPersianNumerals(Math.round(val)),
    },
  },
  grid: {
    borderColor: 'rgba(255, 255, 255, 0.03)',
    strokeDashArray: 5,
    position: 'back',
    yaxis: { lines: { show: true } },
    xaxis: { lines: { show: false } },
  },
  theme: { mode: 'dark' },
  legend: { show: false },
  tooltip: {
    theme: 'dark',
    custom: ({ series, seriesIndex, dataPointIndex, w }: any) => {
      const day   = w.globals.categoryLabels[dataPointIndex]
      const views = toPersianNumerals(series[0][dataPointIndex])
      const downloads = toPersianNumerals(series[1][dataPointIndex])
      return `
        <div class="bg-slate-950/90 backdrop-blur-md border border-white/10 rounded-xl p-3 text-right font-sans" dir="rtl">
          <div class="text-[11px] font-bold text-gray-400 mb-2 border-b border-white/5 pb-1 text-center">${day}</div>
          <div class="flex items-center justify-between gap-6 text-xs text-gray-200 my-1">
            <span class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>بازدید:</span>
            <span class="font-bold text-cyan-400">${views}</span>
          </div>
          <div class="flex items-center justify-between gap-6 text-xs text-gray-200">
            <span class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-[#d4af37]"></span>دانلود:</span>
            <span class="font-bold text-[#d4af37]">${downloads}</span>
          </div>
        </div>
      `
    },
  },
}))
 
// ── Fetch ──────────────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const res = await getDashboardChartService()
    const data = res.data
 
    if (!data || data.days.length === 0) {
      isEmpty.value = true
    } else {
      rawDays.value      = data.days
      rawViews.value     = data.views
      rawDownloads.value = data.downloads
    }
  } catch {
    isEmpty.value = true
  } finally {
    pending.value = false
  }
})
</script>
 
<style scoped>
.text-classic-gold  { color: #d4af37; }
.bg-classic-gold    { background-color: #d4af37; }
.from-classic-gold  {
  --tw-gradient-from: #d4af37 var(--tw-gradient-from-position);
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, rgb(212 175 55 / 0));
}
.to-classic-gold    { --tw-gradient-to: #d4af37 var(--tw-gradient-to-position); }
</style>
