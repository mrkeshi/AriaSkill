<template>
  <div>
      <transition name="slide-up">
      <UiSimpleCard
        v-if="isRegistered"
        title="ثبت نام انجام شد"
        description="جهت فعالسازی حساب کاربری خود لطفا صندوق ایمیل را چک کنید"
        icon="mdi:user"
        to="user-login"
        to-name="بازگشت به صفحه لاگین"
      />
    </transition>
     <div class="min-h-screen flex items-center justify-center p-6 max-md:p-4" dir="rtl">
  

    <div v-if="!isRegistered" class="bg-dark-gray/20 login-card w-full max-md:mt-6 mt-4 max-w-3xl rounded-2xl shadow-xl overflow-hidden">
      
      <div class="p-10 max-md:p-8 space-y-6">
        <div class="text-center space-y-2">
          <h1 class="text-2xl  font-bold text-classic-gold">ایجاد حساب کاربری</h1>
          <p class="text-sm text-bone-white">برای شروع، لطفا اطلاعات زیر را تکمیل کنید.</p>
        </div>

        <Form @submit="sendrequest" v-slot="{ meta, resetForm }" :validation-schema="RegisterSchema" class="space-y-5">
          
          <div class="space-y-4">
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <UiInput
               name="firstName"
                type="text"
                placeholder="علی" 
                v-model="form.first_name"
                :disabled="loading"
                label="نام" rtl>
              </UiInput>

              <UiInput name="lastName"
                type="text"
                placeholder="محمدی" 
                v-model="form.last_name"
                :disabled="loading"
                label="نام خانوادگی" rtl>
              </UiInput>
            </div>

            <UiInput name="username"
              type="text"
              placeholder="ali_mohammadi" 
              v-model="form.username"
              :disabled="loading"
              label="نام کاربری">
            </UiInput>

            <UiInput name="email"
              type="email"
              placeholder="example@mail.com" 
              v-model="form.email"
              :disabled="loading"
              label="ایمیل">
            </UiInput>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <UiInput name="password"
                type="password"
                placeholder="*******" 
                v-model="form.password"
                :disabled="loading"
                label="رمز عبور">
              </UiInput>

              <UiInput name="password_confirm"
                type="password"
                placeholder="*******" 
                v-model="form.password_confirm"
                :disabled="loading"
                label="تکرار رمز عبور">
              </UiInput>
            </div>

          </div>

          <UiButton :disabled="loading" variant="gold" type="submit" full class="mt-6 text-md">
            ثبت‌نام در سایت
          </UiButton>
          
        </Form>

        <div class="relative flex items-center py-2">
          <div class="flex-grow border-t border-gray-200/20"></div>
          <span class="flex-shrink-0 mx-4 text-light-gold text-sm">یا</span>
          <div class="flex-grow border-t border-gray-200/20"></div>
        </div>

        <AuthGoogleButton @credential="registerWithGoogle" />

      </div>


      <div class="bg-dark-gray/5 p-6 text-center border-t border-dark-gray">
        <p class="text-sm text-bone-white">
          قبلاً ثبت‌نام کرده‌اید؟ 
          <NuxtLink :to="{name:'user-login'}" class="font-bold text-classic-gold hover:text-yellow-600 transition ml-1">
            وارد شوید
          </NuxtLink>
        </p>
      </div>

    </div>
  </div>
  </div>
  
 
</template>

<script setup lang="ts">
// @page UserRegister
// This page allows users to register for an account on the website. It includes a form with fields for first name, last name, username, email, password, and password confirmation. The form uses VeeValidate for validation and displays appropriate error messages. Upon successful registration, a success message is shown, and the user is prompted to check their email for account activation. The page also includes an option to register using Google authentication. SEO metadata is generated for better search engine visibility. 
import { reactive, ref } from 'vue'
import { Form } from 'vee-validate';
import type { RegisterDTO } from '~/models/User/AuthDTO';
import { RegisterSchema } from '~/validation/User/UserValidation';
import { generateSeoMeta } from '~/utilities/seo';
import { registerUserService } from '~/services/user/user.Service';
import { useCustomToastify } from '~/composable/useCustomToasitify';

const {showSuccess}=useCustomToastify()
const authStore = useAuthStore()
const loading = ref(false)
const isRegistered=ref(false)
const form: RegisterDTO = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password_confirm: '',
  password: ''
})


const sendrequest =  (_: unknown, { resetForm }: any) => {
  loading.value = true
    registerUserService(form).then((res)=>{
    isRegistered.value=true
    console.log(isRegistered)
    showSuccess({
      title:'ثبت نام',
      message:'با موفقیت انجام شد'
    })
  }).finally(()=>
  loading.value=false)
}

const registerWithGoogle = (credential: string) => {
  loading.value = true
  authStore.loginWithGoogle(credential).finally(() => {
    loading.value = false
  })
}



const seo = generateSeoMeta({
      title: `ثبت نام در آریا کرفت`,
      description: 'در ایند',
      image: "",
      url: ``,
      keywords: ["افزودن پروژه"],
      author:"علیرضا کشاورز",
      type: 'website'
    })
    useHead(seo)
</script>
