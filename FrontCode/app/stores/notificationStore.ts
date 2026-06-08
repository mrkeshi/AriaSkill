import { defineStore } from 'pinia'
import { getUnreadNotificationCountService } from '~/services/notification/notification.Service'

export const useNotificationStore = defineStore('NotificationStore', () => {
  const unreadCount = ref(0)

  const fetchUnreadCount = async () => {
    try {
      const res = await getUnreadNotificationCountService()
      unreadCount.value = res?.data?.unread_count ?? 0
    } catch {
      // silent
    }
  }

  const decrement = (by = 1) => {
    unreadCount.value = Math.max(0, unreadCount.value - by)
  }

  const reset = () => {
    unreadCount.value = 0
  }

  return { unreadCount, fetchUnreadCount, decrement, reset }
})
