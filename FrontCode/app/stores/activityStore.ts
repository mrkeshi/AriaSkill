import { defineStore } from 'pinia'
import { getUnseenActivityCountService } from '~/services/activity/activity.Service'

/**
 * Pinia store to manage the notification/activity count that the user has not seen yet.
 * Useful for updating badge counts in headers, sidebars, or navigation elements.
 */
export const useActivityStore = defineStore('ActivityStore', () => {
  // State: Holds the current number of unseen activities
  const unseenCount = ref(0)

  /**
   * Fetches the latest unseen activities count from the server.
   * Updates the `unseenCount` state, defaulting to 0 on failure or empty response.
   */
  const fetchUnseenCount = async () => {
    try {
      const res = await getUnseenActivityCountService()
      unseenCount.value = res?.data?.unseen_count ?? 0
    } catch {
      // Silently catch errors to prevent breaking the UI flow
    }
  }

  /**
   * Decrements the unseen count by a specified amount (e.g., when a single notification is read).
   * Ensures the count never drops below 0.
   * * @param {number} by - The number to subtract from the total count. Defaults to 1.
   */
  const decrement = (by = 1) => {
    unseenCount.value = Math.max(0, unseenCount.value - by)
  }

  /**
   * Resets the unseen activity count back to 0 (e.g., when clearing all notifications or logging out).
   */
  const reset = () => {
    unseenCount.value = 0
  }

  // Expose state and actions to be utilized across components
  return { unseenCount, fetchUnseenCount, decrement, reset }
})