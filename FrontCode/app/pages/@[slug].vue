<template>
  <div class="min-h-screen text-slate-100 pb-20" dir="rtl">

    <div v-if="pending" class="max-w-7xl mx-auto pt-20 px-4 sm:px-6 lg:px-8 flex flex-col gap-8">
      <SkeletonSimple class="w-full h-64 rounded-3xl" />
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-10">
        <SkeletonSimple class="lg:col-span-2 h-40 rounded-3xl" />
        <SkeletonSimple class="h-40 rounded-3xl" />
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 mt-8">
        <SkeletonSimple v-for="i in 3" :key="i" class="h-80 rounded-3xl" />
      </div>
    </div>

    <div v-else-if="notFound" class="flex flex-col items-center justify-center min-h-[70vh] gap-6 text-center px-4">
      <div class="w-24 h-24 rounded-full bg-slate-900 border border-white/10 flex items-center justify-center mb-2 shadow-[0_0_40px_rgba(212,175,55,0.15)] relative">
        <div class="absolute inset-0 rounded-full border-t-2 border-classic-gold animate-spin-slow"></div>
        <Icon name="mdi:account-search-outline" size="48" class="text-classic-gold opacity-90" />
      </div>
      <h1 class="text-3xl font-black text-white">کاربری پیدا نشد</h1>
      <p class="text-gray-400 max-w-sm text-lg">این نام کاربری وجود ندارد یا حساب کاربری او غیرفعال شده است.</p>
      <NuxtLink to="/">
        <UiButton variant="outline" class="mt-4 px-8 hover:border-classic-gold hover:text-classic-gold transition-all">
          بازگشت به صفحه اصلی
        </UiButton>
      </NuxtLink>
    </div>

    <div v-else-if="profile" class="max-w-7xl mx-auto pt-10 sm:pt-16 px-4 sm:px-6 lg:px-8 flex flex-col gap-8">
      
      <div class="bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 border border-white/10 rounded-[2rem] shadow-2xl relative overflow-hidden group">
        
        <div class="absolute inset-0 opacity-[0.03] animate-grid-shift pointer-events-none" style="background-image: linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px); background-size: 40px 40px;"></div>

        <div class="absolute -top-32 -right-32 w-[30rem] h-[30rem] bg-cyan-500/10 rounded-full blur-[100px] pointer-events-none animate-blob"></div>
        <div class="absolute -bottom-32 -left-32 w-[30rem] h-[30rem] bg-classic-gold/15 rounded-full blur-[100px] pointer-events-none animate-blob animation-delay-2000"></div>

        <div class="relative w-full h-48 sm:h-64 ">
          <!-- یوزرنیم بک‌گراند بزرگ -->
          <div dir="ltr" class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-white/[0.02] text-7xl sm:text-9xl font-black select-none tracking-tighter pointer-events-none font-pelak uppercase w-full text-center transform group-hover:scale-105 transition-transform duration-700">
            @{{ profile.username }}
          </div>
        </div>

        <div class="px-6 sm:px-10 pb-8">
          <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-6 relative z-10">
            
            <div class="flex flex-col sm:flex-row items-center sm:items-end gap-6 sm:gap-8 -mt-20 sm:-mt-24">
              
              <div class="relative w-36 h-36 sm:w-44 sm:h-44 rounded-full p-1.5 bg-carb-gray/10 border border-white/10 shadow-[0_0_30px_rgba(0,0,0,0.8)] shrink-0 group/avatar hover:-translate-y-2 transition-all duration-500">
                <div class="absolute inset-0 rounded-full bg-gradient-to-tr from-classic-gold via-amber-300 to-cyan-500 opacity-50 group-hover/avatar:opacity-100 group-hover/avatar:blur-md transition-all duration-500"></div>
                <div class="relative w-full h-full rounded-full overflow-hidden bg-slate-900 border-[4px] border-slate-950">
                  <img
                    v-if="avatarUrl"
                    :src="avatarUrl"
                    :alt="profile.full_name"
                    class="w-full h-full object-cover group-hover/avatar:scale-110 transition-transform duration-500"
                  />
                  <div
                    v-else
                    class="w-full h-full flex items-center justify-center text-6xl font-black text-classic-gold uppercase bg-gradient-to-br from-slate-800 to-slate-950"
                  >
                    {{ userInitial }}
                  </div>
                </div>
              </div>

              <div class="flex flex-col items-center sm:items-start pb-2 text-center sm:text-right">
                <h1 class="text-3xl sm:text-4xl font-black text-white tracking-tight drop-shadow-lg mb-2">
                  {{ profile.full_name }}
                </h1>
                <div class="flex flex-wrap items-center justify-center sm:justify-start gap-3">
                  <span dir="ltr" class="text-sm text-cyan-400 font-mono bg-white/5 px-3 py-1 rounded-lg border border-white/10 backdrop-blur-md">
                    @{{ profile.username }}
                  </span>
                  <span v-if="profile.job_title" class="text-classic-gold font-bold text-sm bg-white/5 px-3 py-1 rounded-lg border border-white/10 backdrop-blur-md">
                    {{ profile.job_title }}
                  </span>
                </div>
              </div>

            </div>

            <div v-if="socialLinks.length" class="flex items-center justify-center gap-3 lg:pb-3">
              <a
                v-for="link in socialLinks"
                :key="link.key"
                :href="link.url"
                target="_blank"
                rel="noopener noreferrer"
                class="w-12 h-12 rounded-2xl bg-carb-gray border border-white/10 flex items-center justify-center text-gray-400 hover:text-classic-gold hover:border-classic-gold hover:bg-classic-gold/10 hover:-translate-y-1 hover:shadow-[0_0_15px_rgba(212,175,55,0.4)] transition-all duration-300"
                :title="link.label"
              >
                <Icon :name="link.icon" size="24" />
              </a>
            </div>

          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-2">
        
        <div class="lg:col-span-2 bg-carb-gray/10 border border-white/5 rounded-[2rem] p-8 hover:border-classic-gold/20 hover:shadow-[0_0_30px_rgba(212,175,55,0.05)] transition-all duration-300 relative overflow-hidden">
          <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,rgba(212,175,55,0.03)_0%,transparent_70%)]"></div>
          <div class="flex items-center gap-3 mb-6 relative z-10">
            <div class="w-1.5 h-6 bg-gradient-to-b from-cyan-400 to-classic-gold rounded-full shadow-[0_0_8px_rgba(212,175,55,0.5)]"></div>
            <h2 class="text-lg font-bold text-gray-300 uppercase tracking-widest">درباره من</h2>
          </div>
          <p v-if="profile.about_me" class="text-gray-200 text-[16px] leading-9 text-justify relative z-10">
            {{ profile.about_me }}
          </p>
          <p v-else class="text-gray-500 italic relative z-10">این کاربر هنوز چیزی درباره خودش ننوشته است.</p>
        </div>


        <div class="flex flex-col gap-4">

          <div class="relative flex items-center gap-5 p-5 rounded-[2rem] bg-carb-gray/10 border border-white/5 overflow-hidden group hover:border-cyan-500/40 hover:shadow-[0_0_20px_rgba(6,182,212,0.15)] transition-all duration-300">
            <div class="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 flex items-center justify-center shrink-0 group-hover:shadow-[0_0_15px_rgba(6,182,212,0.3)] transition-all duration-300">
              <Icon name="mdi:folder-multiple-outline" size="28" />
            </div>
            <div class="flex flex-col">
              <span class="text-3xl font-black text-white">{{ toPersianNumerals(profile.projects_count) }}</span>
              <span class="text-sm text-gray-400">پروژه منتشرشده</span>
            </div>
            <div class="absolute left-0 top-1/4 bottom-1/4 w-[2px] bg-cyan-400 rounded-r opacity-0 group-hover:opacity-80 transition-all duration-300"></div>
          </div>


          <div class="relative flex items-center gap-5 p-5 rounded-[2rem] bg-carb-gray/10 border border-white/5 overflow-hidden group hover:border-rose-500/40 hover:shadow-[0_0_20px_rgba(244,63,94,0.15)] transition-all duration-300">
            <div class="w-14 h-14 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-400 flex items-center justify-center shrink-0 group-hover:shadow-[0_0_15px_rgba(244,63,94,0.3)] transition-all duration-300">
              <Icon name="mdi:heart-multiple-outline" size="28" />
            </div>
            <div class="flex flex-col">
              <span class="text-3xl font-black text-white">{{ toPersianNumerals(profile.total_likes) }}</span>
              <span class="text-sm text-gray-400">مجموع پسندها</span>
            </div>
            <div class="absolute left-0 top-1/4 bottom-1/4 w-[2px] bg-rose-400 rounded-r opacity-0 group-hover:opacity-80 transition-all duration-300"></div>
          </div>

          <!-- تاریخ عضویت -->
          <div class="relative flex items-center gap-5 p-5 rounded-[2rem] bg-carb-gray/10 border border-white/5 overflow-hidden group hover:border-classic-gold/40 hover:shadow-[0_0_20px_rgba(212,175,55,0.15)] transition-all duration-300">
            <div class="w-14 h-14 rounded-2xl bg-classic-gold/10 border border-classic-gold/20 text-classic-gold flex items-center justify-center shrink-0 group-hover:shadow-[0_0_15px_rgba(212,175,55,0.3)] transition-all duration-300">
              <Icon name="mdi:calendar-month-outline" size="28" />
            </div>
            <div class="flex flex-col">
              <span class="text-lg font-bold text-white">{{ joinDate }}</span>
              <span class="text-sm text-gray-400">تاریخ عضویت</span>
            </div>
            <div class="absolute left-0 top-1/4 bottom-1/4 w-[2px] bg-classic-gold rounded-r opacity-0 group-hover:opacity-80 transition-all duration-300"></div>
          </div>
        </div>
      </div>


      <div class="mt-8">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8 px-2">
          <div class="flex items-center gap-3">
            <div class="w-1.5 h-8 bg-gradient-to-b from-cyan-400 to-classic-gold rounded-full shadow-[0_0_15px_rgba(212,175,55,0.5)]"></div>
            <div>
              <h2 class="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-l from-white via-gray-100 to-gray-300">
                پروژه‌های {{ profile.full_name }}
              </h2>
            </div>
          </div>
          
          <span class="text-sm text-classic-gold bg-classic-gold/5 border border-classic-gold/20 px-4 py-2 rounded-xl text-center shadow-[0_0_10px_rgba(212,175,55,0.05)]">
            {{ toPersianNumerals(profile.projects_count) }} پروژه
          </span>
        </div>

        <div v-if="profile.projects.length === 0" class="text-center py-16 bg-carb-gray/10 rounded-[2rem] border border-white/5 border-dashed">
          <div class="w-20 h-20 rounded-full bg-slate-900 border border-white/10 flex items-center justify-center mx-auto mb-4">
            <Icon name="mdi:folder-search-outline" size="40" class="text-classic-gold opacity-50" />
          </div>
          <p class="text-gray-400 text-lg">هنوز پروژه‌ای منتشر نشده است.</p>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          <PublicProfileProjectCard
            v-for="project in visibleProjects"
            :key="project.id"
            :project="project"
          />
        </div>

        <div v-if="hasMore" class="flex justify-center mt-12">
          <button
            class="flex items-center gap-3 px-8 py-4 rounded-2xl border border-white/10 bg-carb-gray/10 text-gray-300 hover:text-classic-gold hover:border-classic-gold/50 hover:bg-classic-gold/5 hover:shadow-[0_0_20px_rgba(212,175,55,0.15)] transition-all duration-300 text-base font-bold group"
            @click="showAll = true"
          >
            <Icon name="mdi:chevron-down" size="24" class="group-hover:translate-y-1 transition-transform" />
            نمایش همه {{ toPersianNumerals(profile.projects.length) }} پروژه
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
// @page UserProfile
// This page displays the public profile of a user based on their username. It retrieves the username from the route parameters, fetches the user's profile data from the server, and displays it in a
import { ref, computed, onMounted } from 'vue'
import { useRoute, watchEffect } from '#imports'
import { useHead } from '#app'
import { getPublicUserProfileService } from '~/services/user/publicProfile.Service'
import type { PublicUserProfileDTO } from '~/models/User/PublicProfileDTO'
import { toPersianNumerals, toJalaliLong } from '~/utilities/dateHelpers'
import { resolveMediaUrl } from '~/utilities/urlHelpers'
import { generateSeoMeta } from '~/utilities/seo'

const route = useRoute()
const username = computed(() => (route.params.slug as string).replace(/^@/, ''))

const pending  = ref(true)
const notFound = ref(false)
const profile  = ref<PublicUserProfileDTO | null>(null)
const showAll  = ref(false)

const avatarUrl = computed(() =>
  profile.value?.avatar ? resolveMediaUrl(profile.value.avatar) : ''
)

const userInitial = computed(() => {
  const name = profile.value?.full_name || profile.value?.username || ''
  return name.charAt(0).toUpperCase()
})

const joinDate = computed(() =>
  profile.value ? toJalaliLong(profile.value.date_joined) : ''
)

const socialLinks = computed(() => {
  if (!profile.value) return []
  return [
    { key: 'instagram', label: 'اینستاگرام', icon: 'mdi:instagram',        url: profile.value.instagram_link },
    { key: 'telegram',  label: 'تلگرام',      icon: 'mdi:telegram',         url: profile.value.telegram_link  },
    { key: 'linkedin',  label: 'لینکدین',     icon: 'mdi:linkedin',         url: profile.value.linkedin_link  },
    { key: 'discord',   label: 'دیسکورد',     icon: 'mdi:discord',          url: profile.value.discord_link   },
  ].filter(l => !!l.url)
})

const INITIAL_COUNT = 6
const visibleProjects = computed(() =>
  showAll.value
    ? (profile.value?.projects ?? [])
    : (profile.value?.projects ?? []).slice(0, INITIAL_COUNT)
)
const hasMore = computed(() =>
  !showAll.value && (profile.value?.projects.length ?? 0) > INITIAL_COUNT
)

onMounted(async () => {
  try {
    const res = await getPublicUserProfileService(username.value)
    if (res?.data) {
      profile.value = res.data
    } else {
      notFound.value = true
    }
  } catch {
    notFound.value = true
  } finally {
    pending.value = false
  }
})

watchEffect(() => {
  if (!profile.value) return
  const seo = generateSeoMeta({
    title: `${profile.value.full_name} — پروفایل`,
    description: profile.value.about_me ?? `پروفایل ${profile.value.full_name} در آریا کرفت`,
    image: profile.value.avatar ?? '',
    url: `/@${profile.value.username}`,
    keywords: ['پروفایل', profile.value.username, profile.value.job_title ?? ''],
    author: profile.value.full_name,
    type: 'profile',
  })
  useHead(seo)
})
</script>

<style scoped>
.animate-spin-slow {
  animation: spin 3s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes blob {
  0%, 100% { transform: translate(0px, 0px) scale(1); }
  50% { transform: translate(25px, -25px) scale(1.1); }
}
.animate-blob {
  animation: blob 7s infinite ease-in-out;
}
.animation-delay-2000 {
  animation-delay: 2s;
}

@keyframes grid-shift {
  from { background-position: 0 0; }
  to { background-position: 40px 40px; }
}
.animate-grid-shift {
  animation: grid-shift 25s linear infinite;
}
</style>