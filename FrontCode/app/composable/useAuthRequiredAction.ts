import { useCustomToastify } from '~/composable/useCustomToasitify'
import { useAuthStore } from '~/stores/authStore'
// Composable that provides a function to ensure the user is authenticated before performing certain actions, showing a toast notification if authentication is required
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
