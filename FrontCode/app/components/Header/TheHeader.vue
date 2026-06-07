<template>
  <header
    class="sticky top-0 z-50 border-b border-white/5
           bg-[#0A0A0C]/85 backdrop-blur-xl
           shadow-[0_10px_30px_rgba(0,0,0,0.3)]
           transition-all duration-300"
  >
    <div class="container mx-auto px-6 h-20 flex justify-between items-center">

      <div class="flex items-center gap-10">
        <HeaderTheLogo />
        <HeaderTheNavbar />
      </div>

      <div class="flex items-center gap-3 relative">
        <HeaderNotificationDropdown />

        <div class="hidden md:block w-px h-6 bg-gray-700/40"></div>

        <HeaderProfileDropdown />
      </div>

    </div>
  </header>
</template>
