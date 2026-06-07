<template>
  <div>
    <div
      v-for="i in repeat"
      :key="i"
      :class="['animate-pulse rounded-xl bg-white/5 border border-white/8 w-full', $attrs.class]"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  repeat?: number
}>()
</script>
