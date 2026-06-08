import { defineStore } from 'pinia'
import { getUnseenActivityCountService } from '~/services/activity/activity.Service'

export const useActivityStore = defineStore('ActivityStore', () => {
  const unseenCount = ref(0)

  const fetchUnseenCount = async () => {
    try {
      const res = await getUnseenActivityCountService()
      unseenCount.value = res?.data?.unseen_count ?? 0
    } catch {
      // silent
    }
  }

  const decrement = (by = 1) => {
    unseenCount.value = Math.max(0, unseenCount.value - by)
  }

  const reset = () => {
    unseenCount.value = 0
  }

  return { unseenCount, fetchUnseenCount, decrement, reset }
})
