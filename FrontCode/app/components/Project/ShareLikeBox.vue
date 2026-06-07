<template>
<UiCardBlury>
  <div class="flex justify-between">
 <button
   type="button"
   class="like flex items-center gap-1 text-classic-gold"
   :disabled="loading"
   @click="$emit('toggle-like')"
 >

    <svg
      class="transition cursor-pointer stroke-2 stroke-classic-gold hover:fill-classic-gold"
      :class="project.user_has_liked ? 'fill-classic-gold' : 'fill-none'"
      width="26"
      height="26"
      viewBox="0 0 28 28"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M14.373 3.02051C17.377 -0.33962 22.2217 -0.339604 25.2256 3.02051C28.2582 6.41322 28.2585 11.9346 25.2256 15.3271L14.5938 27.2188C14.2587 27.5935 13.7413 27.5935 13.4062 27.2188L2.77441 15.3271C-0.258493 11.9346 -0.258263 6.41324 2.77441 3.02051C5.77835 -0.33962 10.623 -0.339604 13.627 3.02051L14 3.4375L14.373 3.02051Z"
      />
    </svg>

    <span class="font-black -mb-1">
      <span>{{ project.likes_count }}</span> لایک
    </span>

  </button>


  <button type="button" class="share flex items-center gap-1 text-classic-gold cursor-pointer" @click="$emit('share')">
    <Icon name="mdi:share-variant" class="text-[26px]" />

    <span class="font-black -mb-1">اشتراک گذاری</span>

  </button>

  </div>
 
</UiCardBlury>
</template>

<script lang="ts" setup>
import type { ProjectDTO } from '~/models/Project/ProjectDTO'

defineProps<{
  project: ProjectDTO
  loading?: boolean
}>()

defineEmits<{
  'toggle-like': []
  share: []
}>()
</script>
