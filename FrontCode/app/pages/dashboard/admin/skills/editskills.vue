<template>
  <div class="max-w-3xl mx-auto space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-white mb-2">ویرایش مهارت</h2>
      <p class="text-gray-400">اطلاعات مهارت را به‌روزرسانی کنید.</p>
    </div>

    <UiCardBlury class="p-6">
      <Form
        :validation-schema="EditSkillsSchema"
        @submit="submitForm"
        class="grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        <div class="md:col-span-2">
          <UiInput
            rtl
            v-model="form.name"
            name="name"
            label="نام مهارت"
            placeholder="مثال: Vue.js"
          />
        </div>

        <div class="md:col-span-2 flex flex-col sm:flex-row items-start gap-6">
          <div class="flex-1 w-full">
            <UiFileAttachment
              v-model="form.icon as any"
              name="icon"
              label="انتخاب آیکون"
              accept="image/jpeg, image/png"
              hint="فرمت‌های مجاز: JPG, PNG (حداکثر ۲ مگابایت)"
            />
          </div>

          <div
            class="w-32 h-32 shrink-0 bg-white/5 border border-white/10 rounded-2xl flex items-center justify-center overflow-hidden shadow-inner"
          >
            <img
              v-if="imagePreview"
              :src="imagePreview"
              class="w-full h-full object-cover transition-transform duration-300 hover:scale-110"
              alt="پیش‌نمایش آیکون"
            />
            <Icon
              v-else
              name="solar:gallery-bold-duotone"
              class="text-5xl text-gray-500/50"
            />
          </div>
        </div>

        <div class="md:col-span-2 flex justify-end mt-4 pt-4 border-t border-white/5">
          <UiButton
            :disabled="loading || pageLoading"
            variant="gold"
            type="submit"
            full
            class="mt-6 text-md"
          >
            {{ loading ? 'در حال ذخیره...' : 'ذخیره تغییرات' }}
          </UiButton>
        </div>
      </Form>
    </UiCardBlury>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref, watch, onBeforeUnmount, onMounted } from 'vue'
import { Form } from 'vee-validate'
import { EditSkillsSchema } from '~/validation/Skills/CreateSkills'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { retriveSkillsService, editSkillService } from '~/services/skills/skills.Service'

definePageMeta({ layout: 'dashboard' })

useHead({
  title: 'ویرایش مهارت'
})

const loading = ref(false)
const pageLoading = ref(false)
const imagePreview = ref<string | null>(null)

const form = reactive({
  name: '',
  icon:  null
})

const route = useRoute()
const router = useRouter()
const { showSuccess } = useCustomToastify()

const skillId = Number(route.query.id)

watch(
  () => form.icon,
  (newFile) => {
    if (imagePreview.value && imagePreview.value.startsWith('blob:')) {
      URL.revokeObjectURL(imagePreview.value)
    }

    if (newFile instanceof File) {
      imagePreview.value = URL.createObjectURL(newFile)
    }
  }
)

onBeforeUnmount(() => {
  if (imagePreview.value && imagePreview.value.startsWith('blob:')) {
    URL.revokeObjectURL(imagePreview.value)
  }
})

const fetchSkill = async () => {
  if (!skillId) {
    router.push('/dashboard/admin/skills/')
    return
  }

  pageLoading.value = true
  try {
    const res = await retriveSkillsService(skillId)
    const skill = res.data

    form.name = skill.name ?? ''
    form.icon = null
    imagePreview.value = skill.icon ?? null
  } catch (error) {
    console.error('خطا در دریافت مهارت:', error)
    router.push('/dashboard/admin/skills/')
  } finally {
    pageLoading.value = false
  }
}

const submitForm = async () => {
  loading.value = true
  try {
    const formData = new FormData()
    formData.append('name', form.name)

    if (form.icon) {
      formData.append('icon', form.icon)
    }

    await editSkillService(formData, skillId)

    showSuccess({
      title: 'ویرایش مهارت',
      message: 'آیتم با موفقیت ویرایش شد'
    })

    router.push('/dashboard/admin/skills/')
  } catch (error) {
    console.error('خطا در ویرایش مهارت:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchSkill)
</script>
