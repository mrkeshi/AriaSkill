<template>
  <section class="relative w-full py-16 md:pb-8 md:py-16 px-4 md:px-8 bg-transparent overflow-hidden dir-rtl">
    

    <div class="absolute top-1/3 left-10 w-[300px] h-[300px] bg-yellow-500/5 rounded-full blur-[100px] pointer-events-none z-0"></div>

    <div class="max-w-7xl mx-auto flex flex-col-reverse md:flex-row items-center justify-between gap-12 relative z-10">
      
      <div class="flex-1 text-center md:text-right space-y-8">
        
        <div class="space-y-4">
          <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-classic-gold/10 border border-classic-gold/30 text-classic-gold text-xs font-medium tracking-wide animate-pulse">
            ✨ مرکز نوآوری SkillSphere
          </span>
          
          <h1 class="text-4xl md:text-6xl font-black text-bone-white leading-[1.2] md:leading-[1.15]">
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-classic-gold via-yellow-500 to-amber-300 drop-shadow-[0_2px_15px_rgba(212,175,55,0.3)]">
              اکتشاف پروژه‌ها
            </span>
            <br />
            <span class="text-2xl md:text-4xl font-light text-gray-300 tracking-normal block mt-2">
              دنیای بی‌پایان ایده‌ها، یادگیری و خلاقیت
            </span>
          </h1>
        </div>

        <p class="text-gray-400 text-base md:text-lg max-w-xl leading-relaxed mx-auto md:mx-0 font-light">
          با جستجو در میان هزاران پروژه واقعی و چالش‌های تیمی، مسیر یادگیری و توسعه فردی خود را هوشمندانه، هدفمند و بر لبه تکنولوژی بسازید.
        </p>

        <div class="w-full max-w-xl mx-auto md:mx-0 pt-2">
       
        </div>
      </div>

      <div class="flex-1 flex justify-center md:justify-end relative group">
        <div class="absolute inset-0 bg-gradient-to-tr from-classic-gold/10 to-transparent blur-2xl rounded-full opacity-60 group-hover:opacity-80 transition-opacity duration-700"></div>
        
        <img
          src="/images/hero/2.png "
          alt="Explore Projects Hero"
          class="hero-image relative z-10 w-full max-w-[500px] md:max-w-[580px] object-contain drop-shadow-[0_15px_50px_rgba(0,0,0,0.7)]"
        />
      </div>

    </div>
  </section>
</template>

<script lang="ts" setup>
</script>

<style scoped>
.dir-rtl {
  direction: rtl;
}


.hero-image {
  animation: heroFloat 6s ease-in-out infinite;
  will-change: transform;
}

@keyframes heroFloat {
  0%, 100% {
    transform: translateY(0) rotate(0deg) scale(1);
  }
  50% {
    transform: translateY(-12px) rotate(1deg) scale(1.02);
  }
}
</style>