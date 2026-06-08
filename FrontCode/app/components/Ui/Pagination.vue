<script setup>
import { toPersianNumerals } from '~/utilities/dateHelpers'

const props = defineProps({
  totalPages: {
    type: Number,
    required: true
  }
})

const route = useRoute()

const currentPage = computed(() => Number(route.query.page) || 1)

const pages = computed(() => {
  const delta = 2
  const range = []
  
  for (
    let i = Math.max(1, currentPage.value - delta);
    i <= Math.min(props.totalPages, currentPage.value + delta);
    i++
  ) {
    range.push(i)
  }
  return range
})
// Pagination component that displays page numbers with Persian numerals and allows navigation between 
// pages using NuxtLink, showing previous and next buttons when applicable
</script>

<template>
  <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-10">

    <NuxtLink
      v-if="currentPage > 1"
      :to="{ query: { ...route.query, page: currentPage - 1 } }"
      class="px-3 py-2 rounded-lg border border-white/10 bg-white/5 text-gray-300 hover:text-yellow-400 transition"
    >
      <Icon name="mdi:chevron-right" class="mt-1" size="18" />
    </NuxtLink>

    <!-- Requirement #1: Persian numerals in pagination -->
    <NuxtLink
      v-for="page in pages"
      :key="page"
      :to="{ query: { ...route.query, page } }"
      class="min-w-[40px] text-center px-3 py-2 rounded-lg border transition"
      :class="page === currentPage 
        ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500' 
        : 'border-white/10 bg-white/5 text-gray-300 hover:border-yellow-500'"
    >
      {{ toPersianNumerals(page) }}
    </NuxtLink>

    <NuxtLink
      v-if="currentPage < totalPages"
      :to="{ query: { ...route.query, page: currentPage + 1 } }"
      class="px-3 py-2 rounded-lg border border-white/10 bg-white/5 text-gray-300 hover:text-yellow-400 transition"
    >
      <Icon name="mdi:chevron-left" class="mt-1" size="18" />
    </NuxtLink>
    
  </div>
</template>
