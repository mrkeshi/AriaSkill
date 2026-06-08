<template>
  <div class="min-h-screen flex items-center justify-center p-6 max-md:p-4" dir="rtl">
    <div class="bg-dark-gray/20 login-card w-full max-w-md rounded-2xl shadow-xl overflow-hidden">
      
      <div class="p-10 max-md:p-8 space-y-6">
        <div class="text-center space-y-2">
          <h1 class="text-2xl font-bold text-classic-gold">خوش آمدید!</h1>
          <p class="text-sm text-bone-white">لطفا اطلاعات حساب کاربری خود را وارد کنید.</p>
        </div>

        <Form @submit="sendrequest" v-slot="{ meta, resetForm }" :validation-schema="LoginSchema" class="space-y-5">
          <div class="space-y-1">
           
           <UiInput name="identifier"
            type="text"
             placeholder="example@mail.com" 
             v-model="form.identifier"
              :disabled="loading"
              label="ایمیل یا نام کاربری">

            </UiInput>
            <UiInput name="password"
             type="password"
             placeholder="*******" 
             v-model="form.password"
             :disabled="loading"
             label="رمز عبور">
            </UiInput>
          
          </div>

     
          <UiButton :disabled="loading" variant="gold" type="submit" full class="mt-4 text-md">
            ورود به حساب
          </UiButton>
               <div class="">
            <div class="flex items-center justify-between">
            
              <NuxtLink to="/user/forgotpass" class="text-sm text-classic-gold hover:text-yellow-600 transition">
                رمز عبور را فراموش کردید؟
              </NuxtLink>
            </div>
       
          </div>
        </Form>

 
        <div class="relative flex items-center py-2">
          <div class="flex-grow border-t border-gray-200"></div>
          <span class="flex-shrink-0 mx-4 text-light-gold text-sm">یا</span>
          <div class="flex-grow border-t border-gray-200"></div>
        </div>

        <AuthGoogleButton @credential="loginWithGoogle" />

      </div>

      <div class="bg-dark-gray/5 p-6 text-center border-t border-dark-gray">
        <p class="text-sm text-bone-white">
          حساب کاربری ندارید؟ 
          <NuxtLink :to="{name:'user-register'}" class="font-bold text-classic-gold hover:text-yellow-600 transition ml-1">
            ثبت‌نام کنید
          </NuxtLink>
        </p>
      </div>

    </div>
  </div>
</template>

  <script setup lang="ts">
  // @page UserLogin
  // This page allows users to log in to their account using either their email or username and password. It includes form validation using VeeValidate and a Google login option. Upon successful login, the user is redirected to the dashboard. The page also includes SEO metadata for better search engine visibility. 
  import { reactive } from 'vue'
  import type { LoginDTO } from '~/models/User/AuthDTO';
  import { LoginSchema } from '~/validation/User/UserValidation';
  import { Form } from 'vee-validate';
  import { generateSeoMeta } from '~/utilities/seo';
  const loading = ref(false)



const authStore=useAuthStore()


const form:LoginDTO = reactive({
  identifier: '',
  password: ''
})


const sendrequest = (_: unknown, { resetForm }: any) => {
    loading.value = true
    authStore.login(form).finally(()=>{

    loading.value = false
  })

}

const loginWithGoogle = (credential: string) => {
  loading.value = true
  authStore.loginWithGoogle(credential).finally(() => {
    loading.value = false
  })
}



const seo = generateSeoMeta({
      title: `ورود به آریا کرفت`,
      description: 'در ایند',
      image: "",
      url: ``,
      keywords: ["افزودن پروژه"],
      author:"علیرضا کشاورز",
      type: 'website'
    })
    useHead(seo)
</script>
