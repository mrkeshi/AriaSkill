<template>
      <UiAccordingCard title="نوع پروژه">

        <div class="grid grid-cols-1 gap-2 mt-2">
          <UiCheckBox
            v-for="cat in categories"
            :key="cat"
            :name="cat"
            :label="cat"
           :modelValue="filters.category.includes(cat)"
            @update:modelValue="toggleCategory(cat)"
          />
        </div>
      </UiAccordingCard>

</template>

<script lang="ts" setup>
/**
 * - Implements a reactive, accordion-isolated project category filter interface.
 * - Bridges multi-selection states directly to parent component orchestration methods.
 * - Handles resilient array check routines preventing template initialization layout breaks.
 */
import type { ProjectCategory } from '~/models/Project/FilterProjectDTO';
const categories =ref<ProjectCategory[]>([
  "UI/UX Design",
  "Frontend Development",
  "Backend Development",
  "Mobile Development",
  "AI & Data",
  "DevOps & Cloud",
  "Game Development",
  "Cyber Security"
])
const {filters,toggleCategory}=defineProps<{
  filters:{category:ProjectCategory[]},
  toggleCategory: (cat:ProjectCategory) => void
}>()
</script>

<style>

</style>