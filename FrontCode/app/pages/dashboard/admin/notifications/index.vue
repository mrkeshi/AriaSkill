<template>
  <UiCardBlury>

    
    <div class="flex items-start gap-3 mb-8">
      <div class="w-1.5 h-8 bg-gradient-to-b from-purple-400 to-indigo-600 rounded-full mt-1"></div>
      <div>
        <h1 class="text-xl font-black text-white tracking-wide">مدیریت نوتیفیکیشن‌ها</h1>
        <p class="text-xs text-gray-400 mt-1">ارسال پیام همگانی و مشاهده آمار اعلان‌های سیستم</p>
      </div>
    </div>

    <div class="grid lg:grid-cols-5 gap-8">

      
      <div class="lg:col-span-2 space-y-6">

        <div class="bg-white/[0.03] border border-white/10 rounded-2xl p-6 space-y-5">
          <div class="flex items-center gap-3 mb-2">
            <div class="w-9 h-9 rounded-xl bg-purple-500/15 border border-purple-500/20 flex items-center justify-center text-purple-400">
              <Icon name="mdi:bullhorn-outline" size="20" />
            </div>
            <div>
              <h2 class="text-sm font-bold text-white">ارسال پیام همگانی</h2>
              <p class="text-[11px] text-gray-500">به تمام کاربران فعال ارسال می‌شود</p>
            </div>
          </div>

          
          <div>
            <label class="block text-xs font-semibold text-gray-400 mb-1.5">عنوان پیام</label>
            <input
              v-model="form.title"
              type="text"
              placeholder="عنوان پیام همگانی..."
              maxlength="180"
              class="w-full px-4 py-2.5 rounded-xl border border-white/10 bg-white/5 text-white text-sm placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all"
              dir="rtl"
            />
            <p v-if="formErrors.title" class="text-rose-400 text-[11px] mt-1">{{ formErrors.title }}</p>
          </div>

          
          <div>
            <label class="block text-xs font-semibold text-gray-400 mb-1.5">متن پیام</label>
            <textarea
              v-model="form.message"
              rows="5"
              placeholder="متن پیام خود را اینجا بنویسید..."
              maxlength="1000"
              class="w-full px-4 py-2.5 rounded-xl border border-white/10 bg-white/5 text-white text-sm placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all resize-none"
              dir="rtl"
            ></textarea>
            <div class="flex items-center justify-between mt-1">
              <p v-if="formErrors.message" class="text-rose-400 text-[11px]">{{ formErrors.message }}</p>
              <p class="text-[11px] text-gray-600 mr-auto">{{ form.message.length }} / 1000</p>
            </div>
          </div>

          
          <div
            v-if="form.title || form.message"
            class="p-3 rounded-xl border border-purple-500/20 bg-purple-500/5 space-y-1"
          >
            <p class="text-[11px] text-purple-400 font-semibold flex items-center gap-1">
              <Icon name="mdi:eye-outline" size="13" />
              پیش‌نمایش
            </p>
            <p class="text-sm font-bold text-white">{{ form.title || '(بدون عنوان)' }}</p>
            <p class="text-xs text-gray-400 leading-relaxed">{{ form.message || '(بدون متن)' }}</p>
          </div>

          
          <button
            @click="sendBroadcast"
            :disabled="sending"
            class="w-full flex items-center justify-center gap-2 py-3 rounded-xl font-bold text-sm transition-all duration-300"
            :class="sending
              ? 'bg-purple-500/30 text-purple-300 cursor-not-allowed'
              : 'bg-gradient-to-l from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white shadow-[0_0_20px_rgba(168,85,247,0.3)] hover:shadow-[0_0_30px_rgba(168,85,247,0.5)]'"
          >
            <Icon v-if="sending" name="mdi:loading" class="animate-spin" size="18" />
            <Icon v-else name="mdi:send-outline" size="18" />
            {{ sending ? 'در حال ارسال...' : 'ارسال پیام همگانی' }}
          </button>

          
          <Transition name="fade">
            <div
              v-if="lastResult"
              class="p-3 rounded-xl border border-emerald-500/30 bg-emerald-500/10 flex items-center gap-2"
            >
              <Icon name="mdi:check-circle-outline" class="text-emerald-400 shrink-0" size="18" />
              <p class="text-sm text-emerald-300">{{ lastResult }}</p>
            </div>
          </Transition>
        </div>

        
        <div class="grid grid-cols-2 gap-3">
          <div class="bg-white/[0.03] border border-white/10 rounded-xl p-4 text-center">
            <p class="text-2xl font-black text-white font-mono">{{ toPersianNumerals(totalBroadcasts) }}</p>
            <p class="text-[11px] text-gray-500 mt-1">پیام همگانی ارسال‌شده</p>
          </div>
          <div class="bg-white/[0.03] border border-white/10 rounded-xl p-4 text-center">
            <p class="text-2xl font-black text-purple-400 font-mono">{{ toPersianNumerals(totalUnread) }}</p>
            <p class="text-[11px] text-gray-500 mt-1">اعلان خوانده‌نشده (شما)</p>
          </div>
        </div>

      </div>

      
      <div class="lg:col-span-3">
        <div class="bg-white/[0.03] border border-white/10 rounded-2xl p-6">

          
          <div class="flex items-center justify-between mb-5">
            <h2 class="text-sm font-bold text-white flex items-center gap-2">
              <Icon name="mdi:history" size="16" class="text-purple-400" />
              تاریخچه پیام‌های همگانی
            </h2>
            <div class="flex items-center gap-2">
              
              <button
                @click="fetchHistory"
                :disabled="historyLoading"
                class="text-xs text-gray-400 hover:text-white transition flex items-center gap-1"
              >
                <Icon name="mdi:refresh" size="14" :class="historyLoading ? 'animate-spin' : ''" />
                بارگذاری مجدد
              </button>
              
              <button
                v-if="broadcastHistory.length > 0"
                @click="confirmClear"
                :disabled="clearing"
                class="text-xs text-rose-400 hover:text-rose-300 transition flex items-center gap-1 border border-rose-500/20 px-2 py-1 rounded-lg hover:bg-rose-500/10"
              >
                <Icon name="mdi:delete-sweep-outline" size="14" />
                پاک کردن همه لاگ‌ها
              </button>
            </div>
          </div>

          
          <Transition name="fade">
            <div
              v-if="showClearConfirm"
              class="mb-4 p-4 rounded-xl border border-rose-500/30 bg-rose-500/10 space-y-3"
            >
              <p class="text-sm text-rose-300 font-semibold" dir="rtl">
                آیا مطمئن هستید؟ تمام تاریخچه لاگ‌ها برای همه پاک خواهد شد.
              </p>
              <div class="flex gap-2">
                <button
                  @click="clearLogs"
                  :disabled="clearing"
                  class="px-4 py-1.5 rounded-lg text-xs font-bold bg-rose-600 hover:bg-rose-500 text-white transition"
                >
                  {{ clearing ? 'در حال پاک‌سازی...' : 'بله، پاک شود' }}
                </button>
                <button
                  @click="showClearConfirm = false"
                  class="px-4 py-1.5 rounded-lg text-xs font-bold border border-white/10 text-gray-400 hover:text-white transition"
                >
                  انصراف
                </button>
              </div>
            </div>
          </Transition>

          
          <div v-if="historyLoading" class="space-y-3">
            <div v-for="i in 5" :key="i" class="h-16 rounded-xl bg-white/5 animate-pulse"></div>
          </div>

          
          <div
            v-else-if="broadcastHistory.length === 0"
            class="flex flex-col items-center justify-center py-10 text-gray-500"
          >
            <Icon name="mdi:bullhorn-outline" class="text-4xl mb-3 opacity-20" />
            <p class="text-sm">هنوز پیامی ارسال نشده است.</p>
          </div>

          
          <div v-else class="space-y-3">
            <div
              v-for="item in broadcastHistory"
              :key="item.id"
              class="flex items-start gap-3 p-4 rounded-xl border border-white/5 bg-white/[0.02] hover:bg-white/[0.04] transition"
            >
              <div class="w-9 h-9 rounded-xl bg-purple-500/15 border border-purple-500/20 flex items-center justify-center text-purple-400 shrink-0 mt-0.5">
                <Icon name="mdi:bullhorn-outline" size="16" />
              </div>
              <div class="flex-1 min-w-0 text-right" dir="rtl">
                <div class="flex items-start justify-between gap-2">
                  <p class="text-sm font-bold text-white truncate">{{ item.title }}</p>
                  <span class="text-[10px] text-gray-600 whitespace-nowrap shrink-0">
                    {{ relativeTime(item.sent_at) }}
                  </span>
                </div>
                <p class="text-xs text-gray-400 mt-1 line-clamp-2">{{ item.message }}</p>
                <div class="flex items-center gap-3 mt-2">
                  <span class="text-[10px] text-gray-600 flex items-center gap-1">
                    <Icon name="mdi:account-outline" size="11" />
                    {{ item.sent_by_username }}
                  </span>
                  <span class="text-[10px] text-emerald-500/70 flex items-center gap-1">
                    <Icon name="mdi:account-group-outline" size="11" />
                    {{ toPersianNumerals(item.sent_to_count) }} کاربر
                  </span>
                </div>
              </div>
            </div>
          </div>

          
          <div v-if="historyTotalPages > 1" class="flex items-center justify-center gap-3 mt-5">
            <button
              :disabled="historyPage <= 1"
              @click="historyPage--"
              class="px-3 py-1 rounded-lg text-xs border border-white/10 bg-white/5 text-gray-400 hover:text-white transition disabled:opacity-30 disabled:cursor-not-allowed"
            >
              قبلی
            </button>
            <span class="text-xs text-gray-500">{{ historyPage }} / {{ historyTotalPages }}</span>
            <button
              :disabled="historyPage >= historyTotalPages"
              @click="historyPage++"
              class="px-3 py-1 rounded-lg text-xs border border-white/10 bg-white/5 text-gray-400 hover:text-white transition disabled:opacity-30 disabled:cursor-not-allowed"
            >
              بعدی
            </button>
          </div>

        </div>
      </div>
    </div>

  </UiCardBlury>
</template>

<script setup>

import { ref, computed, watch, onMounted } from 'vue'
import { generateSeoMeta } from '~/utilities/seo'
import {
  sendBroadcastService,
  getBroadcastLogService,
  clearBroadcastLogService,
  getUnreadNotificationCountService,
} from '~/services/notification/notification.Service'
import { toPersianNumerals, relativeTime } from '~/utilities/dateHelpers'

definePageMeta({ layout: 'dashboard' })

const seo = generateSeoMeta({
  title: 'مدیریت نوتیفیکیشن‌ها - ادمین',
  description: 'ارسال پیام همگانی و مدیریت نوتیفیکیشن‌ها',
  image: '',
  url: '',
  keywords: ['پیام همگانی', 'نوتیفیکیشن'],
  author: 'علیرضا کشاورز',
  type: 'website',
})
useHead(seo)
const form       = ref({ title: 'پیام همگانی', message: '' })
const formErrors = ref({ title: '', message: '' })
const sending    = ref(false)
const lastResult = ref('')

const validate = () => {
  formErrors.value = { title: '', message: '' }
  let ok = true
  if (!form.value.title.trim()) {
    formErrors.value.title = 'عنوان الزامی است.'
    ok = false
  }
  if (form.value.message.trim().length < 5) {
    formErrors.value.message = 'متن پیام باید حداقل ۵ کاراکتر باشد.'
    ok = false
  }
  return ok
}

const sendBroadcast = async () => {
  if (!validate()) return
  sending.value    = true
  lastResult.value = ''
  try {
    const res  = await sendBroadcastService({
      title:   form.value.title.trim(),
      message: form.value.message.trim(),
    })
    const data = res?.data ?? res
    lastResult.value = data?.detail ?? `پیام برای کاربران ارسال شد.`
    form.value.message = ''
    form.value.title   = 'پیام همگانی'
    historyPage.value = 1
    await fetchHistory()
    setTimeout(() => { lastResult.value = '' }, 6000)
  } catch {  }
  finally  { sending.value = false }
}
const broadcastHistory  = ref([])
const historyLoading    = ref(true)
const historyPage       = ref(1)
const historyTotal      = ref(0)
const PAGE_SIZE         = 8
const historyTotalPages = computed(() => Math.ceil(historyTotal.value / PAGE_SIZE))
const totalBroadcasts   = computed(() => historyTotal.value)

const fetchHistory = async () => {
  historyLoading.value = true
  try {
    const res  = await getBroadcastLogService(historyPage.value)
    const data = res?.data ?? res
    broadcastHistory.value = data?.results ?? []
    historyTotal.value     = data?.count   ?? 0
  } catch {
    broadcastHistory.value = []
  } finally {
    historyLoading.value = false
  }
}

watch(historyPage, fetchHistory)
const showClearConfirm = ref(false)
const clearing         = ref(false)

const confirmClear = () => {
  showClearConfirm.value = true
}

const clearLogs = async () => {
  clearing.value = true
  try {
    await clearBroadcastLogService()
    showClearConfirm.value = false
    historyPage.value = 1
    await fetchHistory()
  } catch {  }
  finally  { clearing.value = false }
}
const totalUnread = ref(0)

onMounted(async () => {
  await fetchHistory()
  try {
    const res = await getUnreadNotificationCountService()
    totalUnread.value = (res?.data ?? res)?.unread_count ?? 0
  } catch {  }
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.4s ease; }
.fade-enter-from, .fade-leave-to       { opacity: 0; }
</style>
