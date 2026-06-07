<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-16 pb-10 border-b border-white/5 mb-10">

    <div class="lg:col-span-2 space-y-8 text-right">
      <div class="space-y-4">
        <span class="text-4xl font-black text-white tracking-wider block">
          Skill<span class="text-transparent bg-clip-text bg-gradient-to-r from-classic-gold to-yellow-400 drop-shadow-[0_0_20px_rgba(212,175,55,0.5)]">Sphere</span>
        </span>
        <p class="text-gray-400 text-base font-light leading-relaxed max-w-md">
          بزرگ‌ترین اکوسیستم شبیه‌سازی پروژه‌های واقعی، کار تیمی و ارتقای تخصص در دنیای برنامه‌نویسی. ما مسیر ورود شما به بازار کار بین‌المللی را هموار می‌کنیم.
        </p>
      </div>

      <div class="space-y-4 max-w-md">
        <p class="text-white text-sm font-bold tracking-wide">عضویت در جریان نوآوری و اخبار پلتفرم</p>
        <div class="flex bg-neutral-900/90 border border-white/10 rounded-2xl p-1.5 focus-within:border-classic-gold focus-within:shadow-[0_0_20px_rgba(212,175,55,0.15)] transition-all duration-500">
          <input type="email" placeholder="آدرس ایمیل معتبر شما..." class="flex-1 bg-transparent border-none outline-none text-base text-bone-white px-4 focus:ring-0"/>
          <button class="px-6 py-3.5 bg-classic-gold text-neutral-950 font-black text-sm rounded-xl shadow-[0_0_15px_rgba(212,175,55,0.3)] hover:bg-yellow-400 transition-all">
            تایید ایمیل
          </button>
        </div>
      </div>
    </div>

    <FooterLinks title="پلتفرم" color="classic-gold" :links="platformLinks"/>
    <FooterLinks title="منابع فنی" color="cyan-400" :links="resourceLinks"/>
    <FooterLinks title="پشتیبانی" color="fuchsia-400" :links="supportLinks"/>

  </div>
</template>

<script setup lang="ts">


const platformLinks = [
  "✨ اکتشاف پروژه‌های مدرن",
  "🏆 چالش‌های تیمی آکادمی",
  "📊 جدول رتبه‌بندی برترین‌ها",
  "💼 فرصت‌های شغلی اختصاصی"
]

const resourceLinks = [
  "مستندات جامع API",
  "قوانین کپی‌رایت مخازن",
  "وبلاگ مهندسی نرم‌افزار",
  "کیت توسعه پلتفرم (SDK)"
]

const supportLinks = [
  "مرکز حل اختلاف تیمی",
  "گزارش باگ و دریافت پاداش",
  "تیکت پشتیبانی سرمایه‌گذاران",
  "اتاق گفتگو و دیسکورد"
]
</script>
