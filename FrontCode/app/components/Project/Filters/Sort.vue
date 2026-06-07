<template>
  <ui-card-blury>
    <div class="flex items-center flex-wrap gap-3">
      <button
        v-for="item in items"
        :key="item.value"
        @click="handleSort(item.value)"
        class="px-7 py-3 min-w-[120px] rounded-lg text-sm transition-all duration-200 border text-center hover:bg-white/10"
        :class="{
          'text-yellow-400 border-yellow-400 bg-yellow-400/10': filters.sort === item.value,
          'text-gray-300 border-white/10': filters.sort !== item.value,
        }"
      >
        {{ item.label }}
      </button>
    </div>
  </ui-card-blury>
</template>

<script lang="ts" setup>
import type { FilterSort } from '~/models/Project/FilterProjectDTO'

const { filters } = defineProps<{
  filters: { sort: string }
}>()

const emit = defineEmits<{ (e: 'sort-changed'): void }>()

const items = [
  { label: 'جدیدترین', value: 'new' },
  { label: 'محبوب‌ترین', value: 'popular' },
  { label: 'بیشترین دانلود', value: 'downloads' },
  { label: 'قدیمی‌ترین', value: 'old' },
]

const handleSort = (val: string) => {
  ;(filters as any).sort = val as FilterSort
  emit('sort-changed')
}
</script>