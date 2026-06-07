<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-deep-black text-bone-white px-6 sm:px-4 text-center"
  >
    <h1 class="text-[80px] sm:text-[120px] font-extrabold text-classic-gold mb-4 leading-none">
      {{ error?.statusCode || 404 }}
    </h1>

    <h2 class="text-2xl sm:text-3xl font-bold mb-2">
      {{ title }}
    </h2>

    <p class="text-dark-gray text-base sm:text-lg mb-8 leading-relaxed  md:w-full">
      {{ message }}
    </p>

    <UiButton  :to="{name:'index'}" effect="glow" loading>
      بازگشت به صفحه اصلی
    </UiButton>

    <div class="mt-20 w-48 h-48 rounded-full bg-classic-gold opacity-10 blur-3xl"></div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ error?: { statusCode?: number; message?: string } }>()

const title = computed(() => {
  const code = props.error?.statusCode || 404
  switch (code) {
    case 400:
      return 'درخواست نامعتبر است!'
    case 403:
      return 'دسترسی غیرمجاز!'
    case 404:
      return 'صفحه مورد نظر پیدا نشد!'
    case 500:
      return 'خطایی در سرور رخ داده است!'
    default:
      return 'مشکلی پیش آمده!'
  }
})

const message = computed(() => {
  const code = props.error?.statusCode || 404
  switch (code) {
    case 400:
      return 'درخواست شما قابل پردازش نیست. لطفاً ورودی‌ها را بررسی کنید.'
    case 403:
      return 'شما اجازه دسترسی به این بخش را ندارید.'
    case 404:
      return 'ممکن است صفحه مورد نظر حذف شده یا آدرس اشتباه باشد.'

    default:
      return props.error?.message || 'یک خطای غیرمنتظره رخ داده است.'
  }
})
</script>
