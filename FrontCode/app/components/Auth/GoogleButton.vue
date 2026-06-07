<template>
  <div class="w-full max-w-full">
    <button
      v-if="isReady"
      type="button"
      :disabled="props.loading"
      class="w-full max-w-full overflow-hidden flex items-center justify-center gap-3 rounded-xl border border-white/20 bg-white/5 hover:bg-white/10 active:scale-[0.98] transition-all duration-200 px-4 py-3 text-bone-white font-medium text-sm cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
      @click="handleClick"
    >
      <svg class="flex-shrink-0" width="18" height="18" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
        <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
        <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
      </svg>
      <span class="truncate">{{ props.loading ? 'در حال ورود...' : 'ادامه با گوگل' }}</span>
    </button>

    <div v-else class="w-full max-w-full h-12 rounded-xl bg-white/5 animate-pulse" />
  </div>
</template>

<script setup lang="ts">
/**
 * Auth/GoogleButton.vue
 * ─────────────────────────────────────────────────────────────────────────────
 * فلو کامل:
 *   ۱. SDK گوگل رو داینامیک لود می‌کنه (بدون npm)
 *   ۲. وقتی کاربر کلیک کنه، popup انتخاب حساب باز می‌شه
 *   ۳. بعد از انتخاب، Google یه id_token (credential) برمیگردونه
 *   ۴. credential رو emit می‌کنه به parent (login.vue یا register.vue)
 *   ۵. parent اون رو به authStore.loginWithGoogle() میده
 *   ۶. authStore از googleAuthService → POST /api/account/google/ میزنه
 *   ۷. Django توکن رو verify می‌کنه، یوزر می‌سازه/پیدا می‌کنه، JWT برمیگردونه
 *   ۸. applyAuth() کوکی ها رو ست می‌کنه → redirect به dashboard
 *
 * هیچ صفحه google-callback نیاز نیست — همه چیز درون همین popup اتفاق میفته.
 * ─────────────────────────────────────────────────────────────────────────────
 */

const props = defineProps<{
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'credential', token: string): void
}>()

// Client ID از nuxt.config.ts → runtimeConfig.public.googleClientId
const config = useRuntimeConfig()
const googleClientId = config.public.googleClientId as string

const isReady = ref(false)

// ─── لود اسکریپت گوگل ────────────────────────────────────────────────────────
const loadScript = (): Promise<void> =>
  new Promise((resolve, reject) => {
    if (typeof window === 'undefined') return resolve()

    // اگه قبلاً لود شده بود
    if ((window as any).google?.accounts?.id) {
      isReady.value = true
      return resolve()
    }

    const script = document.createElement('script')
    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true
    script.defer = true
    script.onload = () => { isReady.value = true; resolve() }
    script.onerror = () => reject(new Error('Google SDK failed to load'))
    document.head.appendChild(script)
  })

// ─── initialize Google Identity Services ─────────────────────────────────────
const initGoogle = () => {
  if (!googleClientId) {
    console.warn('[GoogleButton] NUXT_PUBLIC_GOOGLE_CLIENT_ID خالیه! مقدار رو در .env بذار.')
    return
  }

  ;(window as any).google.accounts.id.initialize({
    client_id: googleClientId,
    // این callback وقتی کاربر حساب انتخاب کنه صدا زده می‌شه
    callback: ({ credential }: { credential: string }) => {
      if (credential) emit('credential', credential)
    },
    auto_select: false,        // انتخاب خودکار حساب رو غیرفعال می‌کنیم
    cancel_on_tap_outside: true,
    ux_mode: 'popup',          // ← مهم: popup نه redirect (نیازی به callback page نیست)
  })
}

// ─── کلیک → نمایش popup ──────────────────────────────────────────────────────
const handleClick = () => {
  const gAccounts = (window as any).google?.accounts?.id
  if (!gAccounts) return

  /*
   * google.accounts.id.prompt() اول سعی می‌کنه One Tap نشون بده.
   * اگه One Tap نشد (قبلاً dismiss شده یا browser بلاکش کرده)،
   * ما مستقیماً renderButton رو روی یه div مخفی رندر می‌کنیم و click می‌زنیم
   * تا popup استاندارد گوگل باز بشه — بدون نیاز به redirect یا callback page.
   */
  gAccounts.prompt((notification: any) => {
    if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
      // Fallback: رندر دکمه مخفی گوگل و کلیک برنامه‌ای
      triggerGoogleButton()
    }
  })
}

// ─── Fallback: دکمه مخفی گوگل ────────────────────────────────────────────────
const triggerGoogleButton = () => {
  const container = document.createElement('div')
  container.style.display = 'none'
  document.body.appendChild(container)

  ;(window as any).google.accounts.id.renderButton(container, {
    type: 'standard',
    size: 'large',
  })

  // دکمه‌ای که گوگل رندر کرد رو پیدا کن و کلیک بزن
  const btn = container.querySelector('div[role="button"]') as HTMLElement | null
  if (btn) {
    btn.click()
  }

  // cleanup
  setTimeout(() => document.body.removeChild(container), 1000)
}

// ─── lifecycle ────────────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    await loadScript()
    initGoogle()
  } catch (err) {
    console.error('[GoogleButton]', err)
  }
})
</script>
