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
* [1] Mount & Load  ──> Dynamically loads Google GIS SDK script.
*         │
* [2] Initialize    ──> Configures Client ID and sets "popup" UX mode.
*         │
* [3] User Click    ──> Invokes Google One Tap prompt.
*         │             └─ Fallback: Simulates click on standard hidden button if prompt fails.
*         │
* [4] Authentication──> User selects account via Google Popup window.
*         │
* [5] Token Emitted ──> Receives `id_token` (credential) and emits it to parent view.
*         │
* [6] Backend Auth  ──> Parent passes token to Django via API endpoint.
*         │
* [7] Complete      ──> Django verifies token, generates JWT, and sets final session cookies.

*/

const props = defineProps<{
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'credential', token: string): void
}>()

const config = useRuntimeConfig()
const googleClientId = config.public.googleClientId as string

const isReady = ref(false)

const loadScript = (): Promise<void> =>
  new Promise((resolve, reject) => {
    if (typeof window === 'undefined') return resolve()

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

/**
 * Initializes the Google Identity Services SDK.
 * Configures the Client ID, sets up the authentication callback,
 * and enforces "popup" UX mode for seamless sign-in.
 */

const initGoogle = () => {
  if (!googleClientId) {
    console.warn('[GoogleButton] NUXT_PUBLIC_GOOGLE_CLIENT_ID is missing! Please set it in .env')
    return
  }

  ;(window as any).google.accounts.id.initialize({
    client_id: googleClientId,
    callback: ({ credential }: { credential: string }) => {
      if (credential) emit('credential', credential)
    },
    auto_select: false,
    cancel_on_tap_outside: true,
    ux_mode: 'popup',
  })
}

/**
 * Handles the custom button click event.
 * Attempts to display the Google One Tap prompt first;
 * falls back to the standard popup if the prompt is skipped or blocked.
 */
const handleClick = () => {
  const gAccounts = (window as any).google?.accounts?.id
  if (!gAccounts) return

  gAccounts.prompt((notification: any) => {
    if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
      triggerGoogleButton()
    }
  })
}

/**
 * Fallback mechanism for Google Sign-In.
 * Dynamically creates a hidden container, renders the official Google button,
 * and programmatically clicks it to bypass browser/SDK restrictions.
 */
const triggerGoogleButton = () => {
  const container = document.createElement('div')
  container.style.display = 'none'
  document.body.appendChild(container)

  ;(window as any).google.accounts.id.renderButton(container, {
    type: 'standard',
    size: 'large',
  })

  const btn = container.querySelector('div[role="button"]') as HTMLElement | null
  if (btn) {
    btn.click()
  }

  setTimeout(() => document.body.removeChild(container), 1000)
}

onMounted(async () => {
  try {
    await loadScript()
    initGoogle()
  } catch (err) {
    console.error('[GoogleButton]', err)
  }
})
</script>