//  This file defines the types for the Toastify data transfer objects (DTOs) in a TypeScript project.
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
