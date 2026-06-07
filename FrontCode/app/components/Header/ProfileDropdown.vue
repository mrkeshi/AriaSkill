<template>
  <div class="relative" v-click-outside="closeDropdown">
    

    <button
      v-if="auth.isLogin"
      @click="isProfileOpen = !isProfileOpen"
      class="flex cursor-pointer items-center gap-2.5 border px-4 py-2 rounded-xl
             text-bone-white text-sm font-semibold
             bg-deep-black transition-all duration-300
             shadow-[0_0_15px_rgba(214,175,55,0.05)]
             hover:shadow-[0_0_20px_rgba(214,175,55,0.2)]"
      :class="isProfileOpen ? 'border-classic-gold' : 'border-classic-gold/30'"
      aria-label="My Account"
    >
      <Icon
        name="mdi:account-circle-outline"
        class="text-xl text-classic-gold"
      />

      <span>حساب من</span>

      <Icon
        name="mdi:chevron-down"
        class="text-base transition-transform duration-300 text-gray-500"
        :class="{ 'rotate-180 text-classic-gold': isProfileOpen }"
      />
    </button>


    <UiButton
      v-else
      :to="{ name: 'user-login' }"
      variant="outline"
      class="border-classic-gold/40 text-bone-white
             hover:bg-classic-gold hover:text-black
             shadow-[0_0_15px_rgba(214,175,55,0.1)]
             transition-all rounded-xl px-5 py-2"
    >
      ثبت نام / ورود
    </UiButton>

    <Transition name="glass-dropdown">
      <div
        v-if="isProfileOpen && auth.isLogin"
        class="absolute left-0 mt-3 w-60
               border border-white/10
               rounded-2xl
               shadow-[0_20px_50px_rgba(0,0,0,0.6)]
               z-50 overflow-hidden
               backdrop-blur-xl
               bg-carb-gray
               transition-all duration-300"
      >
        <div class="p-4 border-b border-white/5 text-center bg-deep-black">
          <p class="text-bone-white text-xs font-medium opacity-90">
            {{ auth.user.first_name }} عزیز، خوش آمدی
          </p>
        </div>

        <!-- Links -->
        <ul class="flex flex-col pt-1.5 pb-1">

          <li>
            <NuxtLink
              to="/dashboard"
              class="flex items-center gap-3 px-4 py-2.5 text-sm
                     text-gray-500
                     hover:bg-deep-black
                     hover:text-light-gold
                     transition-colors"
            >
              <Icon
                name="mdi:view-dashboard-outline"
                class="text-base text-classic-gold"
              />
              داشبورد کاربری
            </NuxtLink>
          </li>

          <li>
            <NuxtLink
              to="/dashboard/projects"
              class="flex items-center gap-3 px-4 py-2.5 text-sm
                     text-gray-500
                     hover:bg-deep-black
                     hover:text-light-gold
                     transition-colors"
            >
              <Icon
                name="mdi:folder-outline"
                class="text-base text-classic-gold"
              />
              پروژه‌های من
            </NuxtLink>
          </li>

          <li
            @click="logout = !logout"
            class="mt-1 border-t border-white/5 pt-1"
          >
            <button
              class="w-full cursor-pointer flex items-center gap-3
                     px-4 py-2.5 text-sm
                     text-error
                     hover:bg-error/10
                     transition-colors font-medium"
            >
              <Icon
                name="mdi:logout"
                class="text-base text-error
                       drop-shadow-[0_0_5px_rgba(244,63,94,0.4)]"
              />
              خروج از سامانه
            </button>
          </li>

        </ul>

        <Confirm
          v-model="logout"
          title="خروج"
          description="آیا برای خروج مطمئن هستید؟"
          @confirm="auth.logout"
        />
      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const auth = useAuthStore()

const isProfileOpen = ref(false)
const logout = ref(false)

const closeDropdown = () => {
  isProfileOpen.value = false
}

const vClickOutside = {
  mounted(el: any, binding: any) {
    el.clickOutsideEvent = (event: Event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el: any) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
}
</script>
