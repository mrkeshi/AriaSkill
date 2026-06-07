```vue
<template>
  <div>
    <transition name="slide-up">
      <SimpleCard
        v-if="showCard"
        title="پسورد تغییر کرد!"
        description="پسورد شما با موفقیت تغییر کرد."
        icon="mdi:lock-outline"
        to="index"
        to-name="بازگشت به صفحه لاگین"
      />
    </transition>

    <div v-if="!showCard" class="min-h-screen flex items-center justify-center p-6 max-md:p-4" dir="rtl">
      <div class="bg-dark-gray/20 login-card w-full max-w-md rounded-2xl shadow-xl overflow-hidden">
        
        <div class="p-10 max-md:p-8 space-y-6">
          
          <div class="text-center space-y-2">
            <h1 class="text-2xl font-bold text-classic-gold">تغییر رمز عبور !</h1>
            <p class="text-sm text-bone-white">
              لطفا رمز عبور جدید را وارد کنید.
            </p>
          </div>

          <Form
            @submit="sendrequest"
            v-slot="{ meta, resetForm }"
            :validation-schema="ChangePasswordSchema"
            class="space-y-5"
          >
            <div class="space-y-1">
              <UiInput
                name="password"
                type="password"
                placeholder="********"
                v-model="pa.password"
                :disabled="loading"
                label="پسورد"
              />
            
              <UiInput
                name="password_confirm"
                type="password"
                placeholder="********"
                v-model="pa.password_confirm"
                :disabled="loading"
                label="تکرار پسورد"
              />
            </div>

            <UiButton
              :disabled="loading"
              variant="gold"
              type="submit"
              full
              class="mt-4 text-md"
            >
              تغییر رمز عبور 
            </UiButton>

          </Form>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref } from 'vue'
import { ChangePasswordSchema } from '~/validation/User/UserValidation'
import { Form } from 'vee-validate'
import SimpleCard from '~/components/Ui/SimpleCard.vue'
import type { ChangePasswordDTO, ResetPassDTO } from '~/models/User/AuthDTO'
import { generateSeoMeta } from '~/utilities/seo'
import { changePasswordService } from '~/services/user/user.Service'
import { useCustomToastify } from '~/composable/useCustomToasitify'
const {showError}=useCustomToastify()
const loading = ref(false)
const showCard = ref(false)
const route=useRoute()
const pa:ChangePasswordDTO=reactive({
  password:'',
  password_confirm:'',
  uid:'',
  token:''
})


  pa.uid=route.params.uid as string
  pa.token=route.params.token as string

const sendrequest =async (_: unknown, { resetForm }: any) => {
  loading.value = true

  try{
    await changePasswordService(pa)
    showCard.value = true
  }catch(e){
    showError({title:"خطا",message:"هنگام تغییر پسورد خطایی ایجاد شد. لطفا دوباره تلاش کنید."})
  }finally{
   loading.value = false
  
  }
  


}
const seo = generateSeoMeta({
      title: `رمز عبور جدید`,
      description: 'در ایند',
      image: "",
      url: ``,
      keywords: ["افزودن پروژه"],
      author:"علیرضا کشاورز",
      type: 'website'
    })
    useHead(seo)

</script>
