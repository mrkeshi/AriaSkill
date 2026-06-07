<template>
  <UiCardBlury
    class="min-h-[65vh] mt-6 lg:mt-12 flex flex-col items-center justify-center text-center
           rounded-3xl p-8 border border-white/10
           shadow-[0_30px_60px_rgba(0,0,0,0.6)]
           relative overflow-hidden select-none bg-deep-black"
    dir="rtl"
  >

    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-72 h-72 bg-classic-gold/5 blur-[120px] rounded-full pointer-events-none"></div>


    <div class="relative group mb-8">
      <div
        class="absolute -inset-4 bg-gradient-to-r from-classic-gold to-amber-500
               rounded-full blur-xl opacity-30
               group-hover:opacity-50 group-hover:scale-110
               transition-all duration-700 animate-pulse"
      ></div>

      <div
        class="relative border border-white/5 p-6 rounded-full
               shadow-inner shadow-black
               flex items-center justify-center
               group-hover:rotate-6 transition-transform duration-500
               bg-deep-black"
      >
        <Icon
          name="mdi:fountain-pen-tip"
          class="text-5xl text-classic-gold
                 drop-shadow-[0_0_15px_rgba(214,175,55,0.6)]"
        />
      </div>
    </div>

    <!-- text -->
    <div class="space-y-3 max-w-md relative z-10">
      <span
        class="text-[10px] font-mono font-black uppercase tracking-widest
               text-classic-gold
               drop-shadow-[0_0_5px_rgba(212,175,55,0.4)]"
      >
        // SYSTEM UPDATE
      </span>

      <h1 class="text-3xl md:text-5xl font-black text-bone-white tracking-tight">
        مخزن <span class="text-classic-gold">وبلاگ فنی</span>
      </h1>

      <h2
        class="text-lg md:text-xl text-cyan-400 font-semibold tracking-wide
               drop-shadow-[0_0_8px_rgba(34,211,238,0.3)]"
      >
        در حال پیکربندی و راه‌اندازی...
      </h2>

      <p class="text-gray-500 text-sm leading-relaxed pt-2 font-light">
        ما در حال آماده‌سازی خطوط کد، مقالات تخصصی و محتوای غنی برای شما هستیم.
        به زودی با دکترین جدید بازمی‌گردیم!
      </p>
    </div>

    <!-- loader -->
    <div
      class="w-64 h-1.5 rounded-full mt-10 overflow-hidden p-[1px]
             border border-white/5 bg-deep-black"
    >
      <div
        class="h-full w-[40%] rounded-full
               bg-gradient-to-r from-classic-gold via-light-gold to-classic-gold
               shadow-[0_0_10px_rgba(214,175,55,0.8)]
               animate-loading-slide"
      ></div>
    </div>
  </UiCardBlury>
</template>

<script setup>
import { generateSeoMeta } from '~/utilities/seo'

const seo = generateSeoMeta({
  title: `وبلاگ - به‌زودی`,
  description: 'در حال آماده‌سازی مقالات تخصصی و پلتفرم وبلاگ',
  image: "",
  url: ``,
  keywords: ["وبلاگ", "آریا کرافت", "مقالات برنامه نویسی"],
  author: "علیرضا کشاورز",
  type: 'website'
})

useHead(seo)
</script>

<style scoped>
@keyframes loading-slide {
  0% { transform: translateX(160%); }
  50% { transform: translateX(-20%); }
  100% { transform: translateX(160%); }
}

.animate-loading-slide {
  animation: loading-slide 2.5s cubic-bezier(0.4,0,0.2,1) infinite;
}
</style>
