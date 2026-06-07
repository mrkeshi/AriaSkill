<template>
  <UiCardBlury dir="rtl">
    <div class="space-y-6">
      <div class="flex items-center justify-between border-b border-white/10 pb-4">
        <div>
          <h2 class="text-2xl font-bold text-white">افزودن پروژه</h2>
          <p class="text-sm text-gray-400 mt-1">اطلاعات پروژه، تصویر، فایل و مهارت‌های مرتبط را وارد کنید.</p>
        </div>
        <Icon name="mdi:rocket-launch-outline" class="text-4xl text-classic-gold" />
      </div>

      <DashboardProjectForm
        :loading="loading"
        submit-label="ثبت پروژه"
        @submit="submitProject"
        @cancel="router.push('/dashboard/projects')"
      />
    </div>
  </UiCardBlury>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { createProjectService } from '~/services/projects/project.Service'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { generateSeoMeta } from '~/utilities/seo'

definePageMeta({ layout: 'dashboard' })

const router = useRouter()
const loading = ref(false)
const { showSuccess } = useCustomToastify()

const submitProject = async (formData: FormData) => {
  loading.value = true
  try {
    await createProjectService(formData)
    showSuccess({ title: 'ثبت پروژه', message: 'پروژه با موفقیت ثبت شد.' })
    router.push('/dashboard/projects')
  } finally {
    loading.value = false
  }
}

useHead(generateSeoMeta({
  title: 'افزودن پروژه',
  description: 'ثبت پروژه جدید',
  image: '',
  url: '',
  keywords: ['project'],
  author: 'AriaSkill',
  type: 'website',
}))
</script>
