<template>
  <div class="flex flex-col items-start gap-1">
    <label
      :for="name + 'id'"
      class="flex items-center gap-3 cursor-pointer select-none text-base font-medium text-gray-200"
    >
      <input
        type="checkbox"
        :id="name + 'id'"
        :name="name"
        :checked="value"
        :disabled="disabled"
        @change="handle"
        class="
          w-5 h-5
          rounded-md
          border border-white/20
          bg-white/5
          cursor-pointer
          transition
          accent-yellow-400
          hover:border-yellow-400
          focus:ring-2 focus:ring-yellow-400/40
          disabled:opacity-40 disabled:cursor-not-allowed
        "
      />

      <span class="leading-none">
        {{ label }}
      </span>
    </label>

    <span
      v-if="!ignoreErrorMessage && errorMessage"
      class="text-red-400 text-sm"
    >
      {{ errorMessage }}
    </span>
  </div>
</template>


<script lang="ts" setup>

// CheckBox component integrated with vee-validate for form validation and error handling

import { useField } from 'vee-validate'

const props = defineProps({
  name: { type: String, required: true },
  modelValue: { type: Boolean, default: false },
  label: { type: String, default: '' },
  ignoreErrorMessage: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue'])

const { errorMessage, value, handleChange, setValue } = useField<boolean>(props.name, undefined, {
  initialValue: props.modelValue,
})

watch(() => props.modelValue, (val) => setValue(val))

function handle(e: Event) {
  const target = e.target as HTMLInputElement
  emit('update:modelValue', target.checked)
  handleChange(e)
}

</script>
