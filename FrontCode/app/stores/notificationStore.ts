import { defineStore } from 'pinia'
import { getUnreadNotificationCountService } from '~/services/notification/notification.Service'

/**
 * Pinia store to manage the global unread notifications counter.
 * Commonly used to update real-time notification badges across the layout.
 */
export const useNotificationStore = defineStore('NotificationStore', () => {
  // State: Holds the current reactive count of unread notifications
  const unreadCount = ref(0)

  /**
   * Dispatches an asynchronous API request to fetch the current unread notification count.
   * Updates state on success, or falls back to 0 on failure.
   */
  const fetchUnreadCount = async () => {
    try {
      const res = await getUnreadNotificationCountService()
      unreadCount.value = res?.data?.unread_count ?? 0
    } catch {
      // Suppress errors to avoid interrupting user workflow
    }
  }

  /**
   * Safely reduces the unread tracker by a fixed quantity.
   * Clamps the final counter value at 0 to avoid negative ranges.
   * @param {number} by - Amount of notifications marked as read. Defaults to 1.
   */
  const decrement = (by = 1) => {
    unreadCount.value = Math.max(0, unreadCount.value - by)
  }

  /**
   * Flushes the state entirely back to zero (e.g., when clicking 'Mark all as read').
   */
  const reset = () => {
    unreadCount.value = 0
  }

  // Expose local states and mutation hooks to components
  return { unreadCount, fetchUnreadCount, decrement, reset }
})