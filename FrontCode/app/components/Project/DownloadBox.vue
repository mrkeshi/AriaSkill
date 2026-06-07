<template>
<ui-card-blury>
        <div class="flex justify-between mb-4">

          <div class="text-center">
            <span class="text-light-gold text-xl font-semibold ">{{ project.download_count }}</span>
            <p class="text-gray-400 text-sm">دانلود</p>
          </div>
          <div class="text-center">

            <span class="text-light-gold text-xl font-semibold">{{ project.view_count }}</span>
            <p class="text-gray-400 text-sm">بازدید</p>
          </div>
          <div class="text-center">

            <span class="text-light-gold text-xl font-semibold">{{ project.likes_count }}</span>
            <p class="text-gray-400 text-sm">پسند</p>
          </div>
 
        </div>

        <UiButton
        icon="mdi:download"
        full
        :disabled="loading"
        variant="gold"
        @click="$emit('download')">
          {{ project.file ? 'دانلود پروژه' : 'فایلی ثبت نشده' }}
        </UiButton>

      </ui-card-blury>
</template>

<script lang="ts" setup>
import type { ProjectDTO } from '~/models/Project/ProjectDTO'

defineProps<{
  project: ProjectDTO
  loading?: boolean
}>()

defineEmits<{
  download: []
}>()
</script>
