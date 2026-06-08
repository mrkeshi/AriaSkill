<template>
  <UiCardBlury dir="rtl">
    <div class="space-y-6">
      <div class="flex items-center justify-between border-b border-white/10 pb-4">
        <div>
          <h2 class="text-2xl font-bold text-white">ویرایش پروژه</h2>
          <p class="text-sm text-gray-400 mt-1">اطلاعات، فایل‌ها و مهارت‌های پروژه را ویرایش کنید.</p>
        </div>
        <Icon name="mdi:pencil-outline" class="text-4xl text-classic-gold" />
      </div>

      <SkeletonSimple v-if="pending" :repeat="4" class="h-16" />

      <DashboardProjectForm
        v-else
        :initial-project="project"
        :loading="loading"
        submit-label="ذخیره تغییرات"
        @submit="submitProject"
        @cancel="router.push('/dashboard/projects')"
      />
    </div>
  </UiCardBlury>
</template>

<script setup lang="ts">
/**
 * @page ProjectMutationCoordinator
 * @description Administrative orchestration script for fetching, re-hydrating, and updating existing project records.
 * Serves as an isolated presentation controller managing reactive parameter keys and binary data delivery.
 * 
 * @logic_flow
 * - Dynamic Key Hydration: Uses a computed `slug` token extracted from current path parameters to drive server-side cached data pools.
 * - Reactive Isolation: Intercepts entity modifications via standard multi-part payload envelopes (`FormData`), keeping local views decoupled.
 * - View Freeze Protection: Binds a standalone operational loop (`loading = true`) across async executions to guard against interface collision.
 * 
 * @data_transport
 * - Query Management: Registers automatic request re-evaluation triggers inside an asynchronous wrapper (`useAsyncData`) watching path modifications.
 * - Contextual Routing: Enforces strict programmatic layout updates via client-side router migrations upon transaction resolution.

 */
import { ref, computed } from 'vue'
import { retrieveProjectService, updateProjectService } from '~/services/projects/project.Service'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { generateSeoMeta } from '~/utilities/seo'

definePageMeta({ layout: 'dashboard' })

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const slug = computed(() => String(route.params.slug || ''))
const { showSuccess } = useCustomToastify()

const { data, pending } = await useAsyncData(
  'edit-project',
  () => retrieveProjectService(slug.value),
  { watch: [slug] }
)

const project = computed(() => data.value?.data ?? null)

const submitProject = async (formData: FormData) => {
  loading.value = true
  try {
    await updateProjectService(slug.value, formData)
    showSuccess({ title: 'ویرایش پروژه', message: 'پروژه با موفقیت ویرایش شد.' })
    router.push('/dashboard/projects')
  } finally {
    loading.value = false
  }
}

useHead(generateSeoMeta({
  title: 'ویرایش پروژه',
  description: 'ویرایش پروژه',
  image: '',
  url: '',
  keywords: ['project'],
  author: 'AriaSkill',
  type: 'website',
}))
</script>
