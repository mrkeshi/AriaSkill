<template>
  <div class="flex justify-center items-center min-h-screen p-4 select-none relative z-10">
    <div class="w-full max-w-4xl transition-all duration-300">
      <UiCardBlury>
        <div class="p-8 max-md:p-4" dir="rtl">
          <div class="login-card w-full rounded-2xl overflow-hidden relative">
            
            <div class="absolute -top-24 -right-24 w-56 h-56 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
            <div class="absolute -bottom-24 -left-24 w-56 h-56 bg-amber-500/5 rounded-full blur-3xl pointer-events-none"></div>

            <div class="space-y-10 relative z-10">
              
              <div class="text-center space-y-3">
                <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-white/5 to-white/[0.01] border border-white/10 shadow-[0_0_20px_rgba(212,175,55,0.05)] text-classic-gold mb-2">
                  <Icon name="mdi:account-edit-outline" size="32" />
                </div>
                <h1 class="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-l from-amber-200 via-classic-gold to-yellow-500 drop-shadow-[0_2px_10px_rgba(212,175,55,0.15)] tracking-wide">
                  ویرایش پروفایل
                </h1>
                <p class="text-xs text-gray-400 max-w-xs mx-auto leading-relaxed">
                  اطلاعات حساب کاربری و شبکه‌های اجتماعی خود را بروزرسانی کنید
                </p>
              </div>

              <div class="flex flex-col items-center gap-4 relative group">
                <div class="relative w-32 h-32 rounded-full p-[3px] bg-gradient-to-tr from-transparent via-classic-gold/40 to-cyan-500/40 shadow-[0_0_30px_rgba(0,0,0,0.5)]">
                  
                  <img
                    v-if="avatarPreview"
                    :src="avatarPreview"
                    class="w-full h-full rounded-full object-cover bg-slate-900"
                    alt="آواتار کاربر"
                  />

                  <div 
                    v-else 
                    class="w-full h-full rounded-full bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 border border-white/5 flex items-center justify-center text-4xl font-black text-classic-gold uppercase tracking-wider"
                  >
                    {{ userInitial }}
                  </div>

                  <div class="absolute bottom-0 left-0 right-0 flex justify-center translate-y-2">
                    <UiFileInput
                      name="avatar"
                      label="آپلود آواتار"
                      v-model="form.avatar"
                      :accept="['image/jpeg','image/png']"
                      :disabled="loading || pageLoading"
                    />
                  </div>

                </div>
                <span class="text-[10px] text-gray-500 mt-2 tracking-wide">فرمت‌های مجاز: JPG, PNG</span>
              </div>

              <Form :validation-schema="editUserSchema" @submit="submit" class="space-y-6">

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <UiInput
                    name="first_name"
                    label="نام"
                    placeholder="مثلا علیرضا"
                    v-model="form.first_name"
                    :disabled="loading || pageLoading"
                    rtl
                  />

                  <UiInput
                    name="last_name"
                    label="نام خانوادگی"
                    placeholder="مثلا کشاورز"
                    v-model="form.last_name"
                    :disabled="loading || pageLoading"
                    rtl
                  />
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  <UiInput
                    name="username"
                    label="نام کاربری"
                    v-model="form.username"
                    :disabled="loading || pageLoading"
                    placeholder="نام کاربریت رو رد کن بیاد"
                    rtl
                  />

                  <UiInput
                    name="email"
                    label="ایمیل (غیرقابل تغییر)"
                    v-model="form.email"
                    disabled
                    rtl
                    class="opacity-60 cursor-not-allowed"
                  />
                </div>

                <UiInput
                  name="job_title"
                  label="عنوان شخصی / تخصص"
                  placeholder="مثلا: توسعه دهنده فول استک"
                  v-model="form.job_title"
                  :disabled="loading || pageLoading"
                  rtl
                />

                <UiTextarea
                  name="about_me"
                  label="درباره من"
                  placeholder="چند خط درباره تخصص‌ها و علاقه‌مندی‌های خودتان بنویسید..."
                  v-model="form.about_me"
                  :disabled="loading || pageLoading"
                  :rows="5"
                  rtl
                />

                <div class="pt-6 border-t border-white/5 space-y-4">
                  <label class="text-sm text-classic-gold/90 font-bold flex items-center gap-2"> 
                    <Icon name="mdi:share-variant-outline" size="18" />
                    شبکه‌های اجتماعی و ارتباطی
                  </label>

                  <div class="p-5 rounded-2xl bg-white/[0.01] border border-white/5 grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div class="w-full">
                      <UiInput
                        label="آدرس اینستاگرام"
                        name="instagram_link"
                        placeholder="instagram.com/username"
                        v-model="form.instagram_link"
                        :disabled="loading || pageLoading"
                      />
                    </div>

                    <div class="w-full">
                      <UiInput
                        label="آدرس تلگرام"
                        name="telegram_link"
                        placeholder="t.me/username"
                        v-model="form.telegram_link"
                        :disabled="loading || pageLoading"
                      />
                    </div>

                    <div class="w-full">
                      <UiInput
                        label="آدرس لینکدین"
                        name="linkedin_link"
                        placeholder="linkedin.com/in/username"
                        v-model="form.linkedin_link"
                        :disabled="loading || pageLoading"
                      />
                    </div>

                    <div class="w-full">
                      <UiInput
                        label="آدرس دیسکورد"
                        name="discord_link"
                        placeholder="discord.com/users/username"
                        v-model="form.discord_link"
                        :disabled="loading || pageLoading"
                      />
                    </div>
                  </div>
                </div>

                <div class="pt-4">
                  <UiButton
                    variant="gold"
                    type="submit"
                    full
                    :disabled="loading || pageLoading"
                    class="h-12 text-sm font-bold shadow-[0_4px_20px_rgba(212,175,55,0.15)] hover:shadow-[0_4px_25px_rgba(212,175,55,0.3)] transition-all duration-300"
                  >
                    <div class="flex items-center justify-center gap-2">
                      <Icon v-if="loading" name="line-md:loading-twotone-loop" size="18" />
                      <Icon v-else name="mdi:check-all" size="18" />
                      <span>{{ loading ? 'در حال ذخیره تغییرات...' : 'ذخیره نهایی اطلاعات' }}</span>
                    </div>
                  </UiButton>
                </div>

              </Form>

            </div>
          </div>
        </div>
      </UiCardBlury>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'dashboard'
})

import { reactive, ref, watch, onBeforeUnmount, onMounted, computed } from 'vue'
import { Form } from 'vee-validate'
import type { EditUserDTO } from '~/models/User/EditUserDTO'
import { editUserSchema } from '~/validation/User/EditUserSchema'
import { editUserService, getEditUserService } from '~/services/user/user.Service'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { useAuthStore } from '~/stores/authStore'
import { generateSeoMeta } from '~/utilities/seo'
import { normalizeSocialLinks, resolveMediaUrl } from '~/utilities/urlHelpers'

const loading = ref(false)
const pageLoading = ref(false)

const avatarPreview = ref<string>('')

const form = reactive<EditUserDTO>({
  avatar: null,
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  job_title: '',
  about_me: '',
  instagram_link: '',
  telegram_link: '',
  linkedin_link: '',
  discord_link: ''
})

const userInitial = computed(() => {
  const name = form.first_name.trim() || form.username.trim()
  return name ? name.charAt(0) : 'U'
})

let objectUrl: string | null = null
const { showSuccess } = useCustomToastify()
const authStore = useAuthStore()

watch(
  (() => form.avatar),
  (file) => {
    if (objectUrl) {
      URL.revokeObjectURL(objectUrl)
      objectUrl = null
    }

    if (file instanceof File) {
      objectUrl = URL.createObjectURL(file)
      avatarPreview.value = objectUrl
    } else if (!file) {
      avatarPreview.value = ''
    }
  }
)

onBeforeUnmount(() => {
  if (objectUrl) URL.revokeObjectURL(objectUrl)
})

const fillForm = (profile: Partial<EditUserDTO>) => {
  form.avatar = null
  form.username = profile.username ?? ''
  form.email = profile.email ?? ''
  form.first_name = profile.first_name ?? ''
  form.last_name = profile.last_name ?? ''
  form.job_title = profile.job_title ?? ''
  form.about_me = profile.about_me ?? ''
  form.instagram_link = profile.instagram_link ?? ''
  form.telegram_link = profile.telegram_link ?? ''
  form.linkedin_link = profile.linkedin_link ?? ''
  form.discord_link = profile.discord_link ?? ''
  const avatar = profile.avatar ?? profile.avatr
  avatarPreview.value = typeof avatar === 'string' && avatar ? resolveMediaUrl(avatar) : ''
}

const fetchProfile = async () => {
  pageLoading.value = true
  try {
    const res = await getEditUserService()
    if (res.data) {
      fillForm(res.data)
    }
  } catch (error) {
    console.error('خطا در دریافت اطلاعات پروفایل:', error)
  } finally {
    pageLoading.value = false
  }
}

const appendField = (formData: FormData, key: keyof EditUserDTO) => {
  const value = form[key]
  formData.append(key, typeof value === 'string' ? value : '')
}

const submit = async () => {
  loading.value = true
  try {
    const formData = new FormData()
    appendField(formData, 'username')
    appendField(formData, 'first_name')
    appendField(formData, 'last_name')
    appendField(formData, 'job_title')
    appendField(formData, 'about_me')

    const socialLinks = normalizeSocialLinks(form)
    formData.append('instagram_link', socialLinks.instagram_link)
    formData.append('telegram_link', socialLinks.telegram_link)
    formData.append('linkedin_link', socialLinks.linkedin_link)
    formData.append('discord_link', socialLinks.discord_link)

    if (form.avatar instanceof File) {
      formData.append('avatar', form.avatar)
    }

    const res = await editUserService(formData)
    if (res.data) {
      fillForm(res.data)
    }
    await authStore.fetchUser()

    showSuccess({
      title: 'ویرایش پروفایل',
      message: 'پروفایل شما با موفقیت بروزرسانی شد.',
    })
  } catch (error) {
    console.error('خطا در ویرایش پروفایل:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchProfile)

const seo = generateSeoMeta({
  title: `ویرایش پروفایل`,
  description: 'در ایند',
  image: "",
  url: ``,
  keywords: ["افزودن پروژه"],
  author:"علیرضا کشاورز",
  type: 'website'
})
useHead(seo)
</script>