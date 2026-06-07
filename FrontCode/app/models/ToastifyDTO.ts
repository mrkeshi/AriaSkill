export type ToastParams = {
  title: string
  message: string
  type?: 'success' | 'error' | 'info' | 'warning' | 'default'
  theme?: 'dark' | 'light' | 'colored' | 'auto'
  autoClose?: number | boolean
  toastId?: string
  icon?: string | false
  rtl?: boolean
  hideProgressBar?: boolean
}
