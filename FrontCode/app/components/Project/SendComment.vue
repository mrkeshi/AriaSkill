<template>
  <UiCardBlury>
    <div v-if="!isLoggedIn" class="flex flex-col items-center justify-center gap-4 py-8 text-center">
      <div class="flex items-center justify-center w-16 h-16 rounded-2xl bg-classic-gold/10 border border-classic-gold/20">
        <Icon name="mdi:lock-outline" class="text-3xl text-classic-gold" />
      </div>
      <p class="text-gray-300 text-sm leading-relaxed">
        برای ثبت نظر باید
        <NuxtLink to="/user/login" class="text-classic-gold hover:underline font-medium">وارد حساب کاربری</NuxtLink>
        خود شوید.
      </p>
    </div>

    <!-- Comment form for authenticated users -->
    <template v-else>
      <h3 class="text-light-gold text-lg mb-4">{{ title }}</h3>
      <Form @submit="sendRequest" v-slot="{ resetForm }" :validation-schema="SendCommentSchema" class="space-y-5">
        <UiTextarea rtl name="message"
                  placeholder="هرچه دل تنگت می‌خواهد بنویس"
                  v-model="form.message"
                  :disabled="loading"
                  label="متن پیغام شما">
        </UiTextarea>
        <div class="flex justify-end mt-4">
          <UiButton type="submit" variant="bracket" class="cursor-pointer" :disabled="loading">
            {{ loading ? 'در حال ارسال...' : 'ارسال نظر' }}
          </UiButton>
        </div>
      </Form>
    </template>
  </UiCardBlury>
</template>

<script lang="ts" setup>
import type { SendCommentDTO } from '~/models/Comment/SendCommentDTO'
import { SendCommentSchema } from '~/validation/Comment/SendComment'
import { Form } from 'vee-validate'

const props = withDefaults(defineProps<{
  parentId?: number | null
  loading?: boolean
  title?: string
}>(), {
  parentId: null,
  loading: false,
  title: 'ثبت نظر',
})

const emit = defineEmits<{
  submit: [Pick<SendCommentDTO, 'message' | 'parent'>, () => void]
}>()

// Requirement #3: Check authentication state
const authStore = useAuthStore()
const isLoggedIn = computed(() => authStore.isLogin)

const form = reactive({
  message: '',
})

const sendRequest = async (_: unknown, { resetForm }: any) => {
  emit('submit', {
    message: form.message,
    parent: props.parentId ?? null,
  }, () => {
    form.message = ''
    resetForm()
  })
}
</script>
