<template>
  <header
    class="sticky top-0 z-30 h-20 backdrop-blur-md bg-slate-950/20 border-b border-white/10 shadow-[0_4px_30px_rgba(0,0,0,0.2)] transition-all duration-300"
    dir="rtl"
  >
    <div class="flex h-full items-center justify-between px-6">
      
      <div class="flex items-center gap-3">
        <div class="w-2 h-5 bg-gradient-to-b from-amber-400 to-classic-gold rounded-full shadow-[0_0_10px_rgba(212,175,55,0.3)]"></div>
        <div class="flex flex-col max-lg:hidden">
          <h1 class="font-black text-gray-100 text-xl tracking-wide">
         {{ greetingText }}
            <span class="text-transparent bg-clip-text bg-gradient-to-br from-amber-400 to-light-gold drop-shadow-[0_2px_8px_rgba(212,175,55,0.2)]">
              {{ displayName }}
            </span>
            عزیز، خوش آمدی 👋
          </h1>
        </div>
      </div>

      <div class="flex items-center gap-4" dir="ltr">
        
        <NuxtLink
          to="/"
          class="flex items-center justify-center w-12 h-12 rounded-xl bg-white/[0.02] border border-white/10 text-gray-400 hover:text-classic-gold hover:border-classic-gold/30 hover:bg-classic-gold/5 shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)] hover:shadow-[0_0_15px_rgba(212,175,55,0.15)] transition-all duration-300 group"
          title="بازگشت به خانه"
        >
          <Icon 
            name="mdi:home-lightning-bolt-outline" 
            size="24" 
            class="transition-transform duration-300 group-hover:scale-110" 
          />
        </NuxtLink>

        <span class="w-[1px] h-6 bg-white/10"></span>

        <NuxtLink
          to="/dashboard/profile"
          class="flex items-center gap-3 rounded-xl p-1 pr-3 border border-transparent transition-all duration-300 group"
        >
          <div class="relative p-[2px] bg-gradient-to-tr from-transparent via-classic-gold/600">
            <img
              v-if="user.avatar"
              :src="user.avatar"
              class="h-11 w-11 rounded-full object-cover bg-yellow-500 border border-classic-gold"
              :alt="displayName"
            >
            <div
              v-else
              class="h-11 w-11 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-classic-gold text-lg font-black uppercase tracking-wider"
            >
              {{ avatarFallback }}
            </div>
          </div>
        </NuxtLink>

      </div>

    </div>
  </header>
</template>

<script setup lang="ts">
/**
 * - Glassmorphism dashboard layout header with real-time reactive scheduling.
 * - Dynamically updates time-of-day Persian greetings every 60 seconds.
 * - Safely handles user avatar display with a smart, fallback initial indicator.
 */

import { computed, onMounted, onUnmounted, ref } from 'vue'
import { getIranGreeting } from '~/utilities/dateHelpers'

const auth = useAuthStore()
const user = auth.user

const displayName = computed(() =>
  user.first_name || user.username || 'کاربر'
)

const avatarFallback = computed(() =>
  (user.first_name?.[0] || user.username?.[0] || 'ک').toUpperCase()
)


const greetingText = ref(getIranGreeting())

let greetingTimer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  greetingTimer = setInterval(() => {
    greetingText.value = getIranGreeting()
  }, 60_000)
})

onUnmounted(() => {
  if (greetingTimer !== null) {
    clearInterval(greetingTimer)
    greetingTimer = null
  }
})
</script>

<style scoped>

</style>
