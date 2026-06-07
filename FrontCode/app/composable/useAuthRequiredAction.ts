import { useCustomToastify } from '~/composable/useCustomToasitify'
import { useAuthStore } from '~/stores/authStore'

export const useAuthRequiredAction = () => {
  const authStore = useAuthStore()
  const { showInfo } = useCustomToastify()

  const ensureAuthenticated = (message = 'برای انجام این کار باید وارد حساب کاربری خود شوید.') => {
    if (authStore.isLogin) return true

    showInfo({
      title: 'ورود لازم است',
      message,
    })

    return false
  }

  return { ensureAuthenticated }
}
