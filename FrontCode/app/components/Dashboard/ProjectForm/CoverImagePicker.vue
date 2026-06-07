<template>
  <div class="space-y-2">
    <label class="text-sm font-medium text-gray-300">تصویر کاور</label>
    <label
      class="relative flex aspect-video cursor-pointer items-center justify-center overflow-hidden rounded-xl border-2 border-dashed border-white/15 bg-white/5 transition hover:border-classic-gold/40 hover:bg-white/8"
    >
      <input
        class="absolute inset-0 opacity-0 cursor-pointer"
        type="file"
        accept="image/*"
        @change="onSelect"
      >
      <img v-if="preview" :src="preview" class="h-full w-full object-cover" alt="پیش‌نمایش تصویر">
      <div v-else class="flex flex-col items-center gap-2 text-sm text-gray-400 pointer-events-none">
        <Icon name="mdi:image-outline" class="text-4xl text-gray-500" />
        <span>انتخاب تصویر کاور</span>
        <span class="text-xs text-gray-600">JPG، PNG، WEBP</span>
      </div>
    </label>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onBeforeUnmount } from 'vue'

const props = defineProps<{
  initialUrl?: string
}>()

const emit = defineEmits<{
  change: [file: File | null]
}>()

const preview = ref(props.initialUrl ?? '')
let objectUrl = ''

watch(() => props.initialUrl, (url) => {
  if (!objectUrl) preview.value = url ?? ''
})

const onSelect = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  if (objectUrl) URL.revokeObjectURL(objectUrl)
  objectUrl = URL.createObjectURL(file)
  preview.value = objectUrl
  emit('change', file)
}

onBeforeUnmount(() => {
  if (objectUrl) URL.revokeObjectURL(objectUrl)
})
</script>
