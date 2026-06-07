<template>
  <UiAccordingCard title="سال انتشار">
    <div v-if="pending" class="grid grid-cols-1 gap-2 mt-3">
      <div
        v-for="i in 3"
        :key="i"
        class="h-7 w-32 rounded bg-white/5 animate-pulse"
      />
    </div>

    <div v-else-if="years.length" class="grid grid-cols-1 gap-2 mt-3">
      <UiCheckBox
        v-for="y in years"
        :key="y"
        :name="`year-${y}`"
        :label="`سال ${y}`"
        :model-value="filters.years.includes(y)"
        @update:modelValue="() => toggleYears(y)"
      />
    </div>

    <p v-else class="text-gray-400 text-sm mt-2">سالی یافت نشد</p>
  </UiAccordingCard>
</template>

<script lang="ts" setup>
import { getProjectYearsService } from '~/services/projects/project.Service'

const years = ref<number[]>([])
const pending = ref(true)

const { toggleYears, filters } = defineProps<{
  filters: { q: string; technology: string[]; years: number[] }
  toggleYears: (years: number) => void
}>()

onMounted(async () => {
  pending.value = true
  try {
    const res = await getProjectYearsService()
    years.value = res?.data?.years ?? []
  } catch (e) {
    console.error('خطا در بارگذاری سال‌ها', e)
    // fallback: چند سال اخیر
    const currentYear = new Date().getFullYear() - 621
    years.value = [currentYear, currentYear - 1, currentYear - 2]
  } finally {
    pending.value = false
  }
})
</script>