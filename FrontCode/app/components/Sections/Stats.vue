<template>
  <section class="pb-16 w-full bg-transparent dir-rtl">
    <div
      class="w-full bg-neutral-950/40 backdrop-blur-md border border-white/5 rounded-3xl px-8 py-10 md:px-12 md:py-8 shadow-[0_15px_50px_rgba(0,0,0,0.5)] relative overflow-hidden"
    >
      <div class="absolute -top-12 -left-12 w-48 h-48 bg-classic-gold/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -bottom-12 -right-12 w-48 h-48 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none"></div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 md:gap-10 relative z-10">

        <div class="flex items-center justify-between p-4 rounded-2xl border border-transparent transition-all duration-500 group hover:bg-neutral-900/30 hover:border-classic-gold/20 hover:shadow-[0_0_25px_rgba(212,175,55,0.15)]">
          <div class="text-right">
            <p class="text-3xl md:text-4xl font-black text-white tracking-tight drop-shadow-[0_0_12px_rgba(212,175,55,0.3)]">
              ۴۰۰<span class="text-classic-gold text-2xl font-light ml-0.5">+</span>
            </p>
            <p class="text-gray-400 text-sm md:text-base font-light mt-1.5 group-hover:text-gray-300 transition-colors">
              کاربر فعال
            </p>
          </div>
          <div
            class="w-14 h-14 flex items-center justify-center rounded-2xl bg-classic-gold/10 border border-classic-gold/20 text-classic-gold shadow-[0_0_15px_rgba(212,175,55,0.1)] group-hover:bg-classic-gold group-hover:text-black group-hover:shadow-[0_0_20px_rgba(212,175,55,0.5)] transition-all duration-500 transform group-hover:scale-105"
          >
            <Icon name="mdi:account-group-outline" size="28" />
          </div>
        </div>

        <div class="flex items-center justify-between p-4 rounded-2xl border border-transparent transition-all duration-500 group hover:bg-neutral-900/30 hover:border-cyan-500/20 hover:shadow-[0_0_25px_rgba(6,182,212,0.15)]">
          <div class="text-right">
            <p class="text-3xl md:text-4xl font-black text-white tracking-tight drop-shadow-[0_0_12px_rgba(6,182,212,0.3)]">
              ۳,۵۰۰<span class="text-cyan-400 text-2xl font-light ml-0.5">+</span>
            </p>
            <p class="text-gray-400 text-sm md:text-base font-light mt-1.5 group-hover:text-gray-300 transition-colors">
              مخزن کد
            </p>
          </div>
          <div
            class="w-14 h-14 flex items-center justify-center rounded-2xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.1)] group-hover:bg-cyan-400 group-hover:text-black group-hover:shadow-[0_0_20px_rgba(6,182,212,0.5)] transition-all duration-500 transform group-hover:scale-105"
          >
            <Icon name="mdi:source-repository-multiple" size="28" />
          </div>
        </div>

        <div class="flex items-center justify-between p-4 rounded-2xl border border-transparent transition-all duration-500 group hover:bg-neutral-900/30 hover:border-fuchsia-500/20 hover:shadow-[0_0_25px_rgba(217,70,239,0.15)]">
          <div class="text-right">
            <p class="text-3xl md:text-4xl font-black text-white tracking-tight drop-shadow-[0_0_12px_rgba(217,70,239,0.3)]">
              ۲۴,۵۰۰
            </p>
            <p class="text-gray-400 text-sm md:text-base font-light mt-1.5 group-hover:text-gray-300 transition-colors">
              دانلود موفق
            </p>
          </div>
          <div
            class="w-14 h-14 flex items-center justify-center rounded-2xl bg-fuchsia-500/10 border border-fuchsia-500/20 text-fuchsia-400 shadow-[0_0_15px_rgba(217,70,239,0.1)] group-hover:bg-fuchsia-400 group-hover:text-black group-hover:shadow-[0_0_20px_rgba(217,70,239,0.5)] transition-all duration-500 transform group-hover:scale-105"
          >
            <Icon name="mdi:download-outline" size="28" />
          </div>
        </div>

        <div class="flex items-center justify-between p-4 rounded-2xl border border-transparent transition-all duration-500 group hover:bg-neutral-900/30 hover:border-emerald-500/20 hover:shadow-[0_0_25px_rgba(16,185,129,0.15)]">
          <div class="text-right">
            <p class="text-3xl md:text-4xl font-black text-white tracking-tight drop-shadow-[0_0_12px_rgba(16,185,129,0.3)]">
              ۲۵<span class="text-emerald-400 text-2xl font-light ml-0.5">+</span>
            </p>
            <p class="text-gray-400 text-sm md:text-base font-light mt-1.5 group-hover:text-gray-300 transition-colors">
              حوزه تخصصی
            </p>
          </div>
          <div
            class="w-14 h-14 flex items-center justify-center rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.1)] group-hover:bg-emerald-400 group-hover:text-black group-hover:shadow-[0_0_20px_rgba(16,185,129,0.5)] transition-all duration-500 transform group-hover:scale-105"
          >
            <Icon name="mdi:book-outline" size="28" />
          </div>
        </div>

      </div>
    </div>
  </section>
</template>
<!-- Hero Explore Stats Section -->
<script lang="ts" setup>
</script>

<style scoped>
.dir-rtl {
  direction: rtl;
}
</style>