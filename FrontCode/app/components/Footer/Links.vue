<template>
  <div class="space-y-6 text-right pt-2">
    <h4 :class="`text-white font-black text-lg tracking-wide border-r-4 pr-3 border-${color}`">
      {{ title }}
    </h4>
    <ul class="space-y-4 text-base font-light text-gray-400">
      <li v-for="link in links" :key="link">
        <a href="#" :class="`hover:text-${color} hover:translate-x-[-4px] transition-all duration-300 inline-block`">
          {{ link }}
        </a>
      </li>
    </ul>
  </div>
</template>
<!-- footer component -->

<script setup lang="ts">

defineProps<{
  title: string
  color: string
  links: string[]
}>()
</script>
