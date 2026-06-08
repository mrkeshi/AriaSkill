<template>
       <section class="flex flex-col-reverse md:flex-row items-center justify-between gap-8 py-24 md:py-24 overflow-hidden">
        <div class="flex-1 text-center md:text-right space-y-8">
         <h1 class="text-classic-gold text-4xl md:text-6xl font-pelak font-bold leading-tight text-shine">
  SkillSphere
  <br />
  <span class="text-bone-white text-2xl md:text-4xl">
    دنیای مهارت و همکاری
  </span>
</h1>

          <p class="text-dark-gray text-lg md:text-xl max-w-2xl leading-relaxed mx-auto md:mx-0">
            پلتفرم جامع برای نمایش پورتفولیو، مدیریت پروژه‌های تیمی و یادگیری مدرن‌ترین تکنولوژی‌های روز. مسیر حرفه‌ای خود را از اینجا بسازید.
          </p>
          <div class="flex flex-wrap justify-center md:justify-start gap-4 pt-4">
            <UiButton
              variant="gold"
              :to="{ name: 'user-login' }"
              icon="mdi:login"
            >
              شروع 
            </UiButton>

            <UiButton
              variant="outline"
              to="/explore"
               icon="mdi:magnify"
            >
              جستجوی پروژه‌ها
            </UiButton>
          </div>
        </div>

        <div class="flex-1 flex justify-center md:justify-end relative">
      
<img
  src="/images/hero/1.png"
  alt="SkillSphere Hero"
  class="hero-image relative z-10 w-full max-w-[620px] md:max-w-[720px] object-contain"
/>

        </div>
      </section>


</template>
<!-- Hero HomPage Section -->
<script lang="ts" setup>

</script>

<style>
.hero-image{
  animation: heroFloat 4s ease-in-out infinite;
}

@keyframes heroFloat {
  0% {
    transform: scale(1) rotate(0deg);
  }
  50% {
    transform: scale(1.03) rotate(0.8deg);
  }
  100% {
    transform: scale(1) rotate(0deg);
  }
}

</style>