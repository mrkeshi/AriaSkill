<template>
  <div class="space-y-2 w-full">
    <label class="flex items-center gap-2 cursor-pointer min-w-28 min-h-10 transition ease-in hover:opacity-85 rounded-2xl p-1 justify-center  bg-classic-gold text-black">
      <Icon name="mdi:account-circle-outline" class="w-5 h-5" />
      {{ label }}

      <input
        type="file"
        class="hidden"
        :accept="acceptString"
        :disabled="disabled"
        @change="handle"
      />
    </label>

    <span
      v-if="errorMessage && !ignoreErrorMessage"
      class="text-error text-sm block"
    >
      {{ errorMessage }}
    </span>
  </div>
</template>

<script setup lang="ts">
// FileInput component integrated with vee-validate for form validation and error handling, allowing users to select files with specified types and displaying error messages when necessary
import { useField } from 'vee-validate'
import { watch } from 'vue'
import type { PropType } from 'vue'

const props = defineProps({
  name: { type: String, required: true },

  modelValue: { type: File as PropType<File | null>, default: null },

  label: { type: String, default: 'انتخاب آواتار' },

  accept: { type: Array as PropType<string[]>, default: () => ['image/*'] },

  disabled: { type: Boolean, default: false },

  ignoreErrorMessage: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue'])

const { errorMessage, value, handleChange, setValue } = useField(
  props.name,
  undefined,
  {
    initialValue: props.modelValue
  }
)

watch(() => props.modelValue, (val) => setValue(val))

const acceptString = props.accept.join(',')

const handle = (e: Event) => {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0] || null

  emit('update:modelValue', file)
  setValue(file)
}
</script>
