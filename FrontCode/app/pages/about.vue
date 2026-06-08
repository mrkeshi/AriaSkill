<template>
  <UiCardBlury
    class="my-8 lg:my-12 rounded-[32px] border border-white/10
           shadow-[0_30px_70px_rgba(0,0,0,0.8)]
           relative overflow-hidden select-none bg-deep-black"
    dir="rtl"
  >
    <div class="absolute top-0 right-0 w-80 h-80 bg-classic-gold/5 blur-[120px] rounded-full pointer-events-none"></div>
    <div class="absolute bottom-0 left-0 w-80 h-80 bg-fuchsia-500/5 blur-[120px] rounded-full pointer-events-none"></div>

    <div class="max-w-4xl mx-auto py-8 px-4 md:px-0 relative z-10">

      <!-- header -->
      <div class="flex flex-col items-center text-center mb-16">

        <div class="relative group mb-6">
          <div
            class="absolute -inset-2 bg-gradient-to-r from-classic-gold to-amber-600
                   rounded-full blur-xl opacity-20 group-hover:opacity-40
                   transition-all duration-700 animate-pulse"
          ></div>

          <div
            class="relative border border-white/5 shadow-2xl shadow-black
                   rounded-full p-6 flex items-center justify-center
                   w-28 h-28 transform transition-all duration-500
                   hover:scale-105 group-hover:border-classic-gold/40
                   bg-deep-black"
          >
            <img
              src="/images/logoA.png"
              alt="Logo"
              class="w-full h-full object-contain absolute inset-0 p-6 opacity-20"
            />
            <Icon
              name="mdi:hexagon-multiple"
              class="text-5xl text-classic-gold
                     drop-shadow-[0_0_10px_rgba(214,175,55,0.5)]"
            />
          </div>
        </div>

        <span
          class="text-[10px] font-mono font-black uppercase tracking-widest
                 text-classic-gold"
        >
          // ECOSYSTEM PROFILE
        </span>

        <h1 class="text-3xl md:text-5xl font-black text-bone-white mt-2 mb-4 tracking-tight">
          درباره
          <span
            class="text-transparent bg-clip-text
                   bg-gradient-to-r from-classic-gold to-light-gold"
          >
            آریا کرافت
          </span>
        </h1>

        <p class="text-gray-500 max-w-2xl text-sm leading-relaxed font-light">
          شکل‌دهی به آینده توسعه نرم‌افزار از طریق اشتراک‌گذاری خلاقانه پروژه‌ها،
          مهارت‌ها و کدهای منبع بر لبه تکنولوژی.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">

        <div
          class="border border-white/5 rounded-2xl p-6
                 transition-all duration-500
                 hover:border-classic-gold/30 hover:-translate-y-1
                 group/card bg-deep-black"
        >
          <div class="flex items-center gap-3 mb-4">
            <div
              class="p-2.5 rounded-xl border border-white/5
                     text-classic-gold bg-white/[0.01]
                     group-hover/card:bg-classic-gold
                     group-hover/card:text-black
                     transition-all duration-300"
            >
              <Icon name="mdi:book-open-page-variant-outline" class="text-xl" />
            </div>

            <h3 class="text-lg font-bold text-bone-white">داستان ما</h3>
          </div>

          <p class="text-gray-500 text-xs md:text-sm leading-loose text-justify font-light
                    group-hover/card:text-gray-300 transition-colors">
            لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ...
          </p>
        </div>

        <div
          class="border border-white/5 rounded-2xl p-6
                 transition-all duration-500
                 hover:border-fuchsia-500/30 hover:-translate-y-1
                 group/card bg-deep-black"
        >
          <div class="flex items-center gap-3 mb-4">
            <div
              class="p-2.5 rounded-xl border border-white/5
                     text-fuchsia-400 bg-white/[0.01]
                     group-hover/card:bg-fuchsia-500
                     group-hover/card:text-black
                     transition-all duration-300"
            >
              <Icon name="mdi:telescope" class="text-xl" />
            </div>

            <h3 class="text-lg font-bold text-bone-white">چشم‌انداز</h3>
          </div>

          <p class="text-gray-500 text-xs md:text-sm leading-loose text-justify font-light
                    group-hover/card:text-gray-300 transition-colors">
            شناخت فراوان جامعه و متخصصان را می طلبد...
          </p>
        </div>

      </div>

      <!-- values -->
      <div class="mt-12 border-t border-white/5 pt-12">
        <div class="text-center mb-10">
          <h3 class="text-xl font-black text-bone-white tracking-wide">
            ارزش‌های بنیادین ما
          </h3>
          <div
            class="w-12 h-[2px] bg-classic-gold mx-auto mt-2 rounded-full
                   shadow-[0_0_8px_rgba(214,175,55,0.8)]"
          ></div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">

          <div
            class="flex flex-col items-center text-center p-5 rounded-2xl
                   border border-transparent
                   hover:border-white/5 hover:bg-black/20
                   transition-all duration-300 group/item"
          >
            <Icon
              name="mdi:lightbulb-on-outline"
              class="text-4xl text-classic-gold mb-4
                     drop-shadow-[0_0_10px_rgba(214,175,55,0.3)]
                     group-hover/item:scale-110 transition-transform"
            />
            <h4 class="text-bone-white font-bold text-sm mb-2">نوآوری و خلاقیت</h4>
            <p class="text-gray-500 text-xs leading-relaxed font-light">
              توسعه راهکارهای هوشمندانه و بازتعریف مداوم استانداردهای طراحی نرم‌افزار.
            </p>
          </div>

          <div
            class="flex flex-col items-center text-center p-5 rounded-2xl
                   border border-transparent
                   hover:border-white/5 hover:bg-black/20
                   transition-all duration-300 group/item"
          >
            <Icon
              name="mdi:shield-check-outline"
              class="text-4xl text-cyan-400 mb-4
                     drop-shadow-[0_0_10px_rgba(34,211,238,0.3)]
                     group-hover/item:scale-110 transition-transform"
            />
            <h4 class="text-bone-white font-bold text-sm mb-2">کیفیت و امنیت</h4>
            <p class="text-gray-500 text-xs leading-relaxed font-light">
              پایبندی به کدهای تمیز و معماری مقیاس‌پذیر.
            </p>
          </div>

          <div
            class="flex flex-col items-center text-center p-5 rounded-2xl
                   border border-transparent
                   hover:border-white/5 hover:bg-black/20
                   transition-all duration-300 group/item"
          >
            <Icon
              name="mdi:account-group-outline"
              class="text-4xl text-fuchsia-400 mb-4
                     drop-shadow-[0_0_10px_rgba(217,70,239,0.3)]
                     group-hover/item:scale-110 transition-transform"
            />
            <h4 class="text-bone-white font-bold text-sm mb-2">تعهد به کامیونیتی</h4>
            <p class="text-gray-500 text-xs leading-relaxed font-light">
              ایجاد بستری پویا برای رشد و اشتراک دانش برنامه‌نویسی.
            </p>
          </div>

        </div>
      </div>

      <!-- CTA -->
      <div
        class="mt-16 border border-white/5 rounded-2xl p-6
               flex flex-col sm:flex-row items-center justify-between gap-6
               shadow-inner bg-deep-black"
      >
        <div class="text-center sm:text-right">
          <h4 class="text-bone-white font-black text-lg mb-1 tracking-wide">
            آماده خلق یک اثر هنری جدید هستید؟
          </h4>
          <p class="text-gray-500 text-xs md:text-sm font-light">
            به اکوسیستم ملحق شوید و کدهای خود را متمایز کنید.
          </p>
        </div>

        <button
          class="px-6 py-3 rounded-xl bg-classic-gold text-neutral-950
                 font-black text-xs tracking-wider
                 hover:bg-light-gold
                 shadow-[0_0_15px_rgba(214,175,55,0.3)]
                 hover:shadow-[0_0_25px_rgba(214,175,55,0.6)]
                 hover:scale-[1.03] active:scale-95
                 transition-all duration-300 flex items-center gap-2
                 whitespace-nowrap cursor-pointer"
        >
          <Icon name="mdi:email-outline" class="text-base" />
          <span>برقراری ارتباط فوری</span>
        </button>
      </div>

    </div>
  </UiCardBlury>
</template>
