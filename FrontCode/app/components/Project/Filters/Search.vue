<template>
 
  <UiAccordingCard title="جستجو" :is-open="!!filters.q" >
        <div
          class="w-full flex items-center gap-3 px-5 py-3 rounded-xl bg-black/20 backdrop-blur-md border border-white/10 hover:border-classic-gold/40 transition"
          dir="rtl"
        >
          <input
            maxlength="100"
            type="text"
            
           v-model="filters.q"
            @keyup.enter="applyFilter"
            placeholder="جستجو بین پروژه‌ها، تکنولوژی‌ها و ایده‌ها..."
            class="flex-1 bg-transparent border-none outline-none text-bone-white
                   placeholder-gray-400  text-md"
          />

          <div
            class="w-12 h-12 flex -ml-2 items-center justify-center rounded-full bg-classic-gold/20
                   text-classic-gold group-hover:bg-classic-gold/30 transition cursor-pointer"
            @click="applyFilter"
          >
            <Icon name="mdi:magnify"  size="28" />
          </div>
        </div>
      </UiAccordingCard>
</template>

<script lang="ts" setup>
/**
 * - Implements a reactive search query formulation input field wrapped in an accordion card.
 * - Synchronizes active routing criteria metrics directly via conditional micro-macro bindings.
 * - Leverages contextual ancestor hover group chains triggers maximizing tactile visual micro-interactions.
 */
const {filters,applyFilter} = defineProps<{
  filters: { q: string | undefined  }
  applyFilter: () => void
}>()
</script>

<style>

</style>