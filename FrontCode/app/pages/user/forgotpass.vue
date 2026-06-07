```vue
<template>
  <div>
    <transition name="slide-up">
      <SimpleCard
        v-if="showCard"
        title="ایمیل ارسال شد!"
        description="لینک بازیابی رمز عبور با موفقیت برای شما ارسال شد. لطفا صندوق ورودی و پوشه اسپم (Spam) ایمیل خود را بررسی کنید."
        icon="mdi:email-send-outline"
        to="user-login"
        to-name="بازگشت به صفحه لاگین"
      />
    </transition>

    <div v-if="!showCard" class="min-h-screen flex items-center justify-center p-6 max-md:p-4" dir="rtl">
      <div class="bg-dark-gray/20 login-card w-full max-w-md rounded-2xl shadow-xl overflow-hidden">
        
        <div class="p-10 max-md:p-8 space-y-6">
          
          <div class="text-center space-y-2">
            <h1 class="text-2xl font-bold text-classic-gold">بازیابی پسورد!</h1>
            <p class="text-sm text-bone-white">
              لطفا جهت بازیابی آدرس ایمیل خود را وارد نمایید.
            </p>
          </div>

          <Form
            @submit="sendrequest"
            v-slot="{ meta, resetForm }"
            :validation-schema="ResetPassowrdWithEmailSchema"
            class="space-y-5"
          >
            <div class="space-y-1">
              <UiInput
                name="email"
                type="email"
                placeholder="example@mail.com"
                v-model="email"
                :disabled="loading"
                label="ایمیل"
              />
            </div>

            <UiButton
              :disabled="loading"
              variant="gold"
              type="submit"
              full
              class="mt-4 text-md"
            >
              ارسال لینک بازیابی پسورد
            </UiButton>

          </Form>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref } from 'vue'
import { ResetPassowrdWithEmailSchema } from '~/validation/User/UserValidation'
import { Form } from 'vee-validate'
import SimpleCard from '~/components/Ui/SimpleCard.vue'
import { generateSeoMeta } from '~/utilities/seo'
import { sendResetLinkPassService } from '~/services/user/user.Service'

const loading = ref(false)
const showCard = ref(false)
const email= ref<string>('')



const sendrequest = (_: unknown, { resetForm }: any) => {
  loading.value = true

   sendResetLinkPassService(email.value).then((_)=>{
    showCard.value=true
  }).finally(()=>{
  loading.value = false

  })


}








const seo = generateSeoMeta({
      title: `فراموشی رمز عبور`,
      description: 'در ایند',
      image: "",
      url: ``,
      keywords: ["افزودن پروژه"],
      author:"علیرضا کشاورز",
      type: 'website'
    })
    useHead(seo)
</script>
