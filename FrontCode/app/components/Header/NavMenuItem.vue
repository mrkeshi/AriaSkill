<template>
  <li>
    <NuxtLink 
      :to="to" 
      class="flex items-center gap-2 text-bone-white hover:text-light-gold transition-all duration-300 group py-1.5 px-3 rounded-xl hover:bg-white/[0.02]"
    >
      <Icon 
        :name="icon" 
        class="text-xl text-classic-gold drop-shadow-[0_0_8px_rgba(214,175,55,0.4)] group-hover:scale-110 transition-transform duration-300" 
      />
      <span class="text-sm font-medium tracking-wide">{{ label }}</span>
    </NuxtLink>
  </li>
</template>

<script setup lang="ts">
defineProps<{
  to: string
  icon: string
  label: string
}>()
</script>
