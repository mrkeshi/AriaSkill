<template>
  <Transition name="overlay">
    <div
      v-if="modelValue"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
    >
      <Transition name="modal">
        <div
          v-if="modelValue"
          class="w-full max-w-md mx-4 rounded-2xl border border-white/10 bg-black/60 backdrop-blur-xl p-8 shadow-xl"
        >
          <h2 class="text-xl font-bold text-bone-white text-center">
            {{ title }}
          </h2>

          <p v-if="description" class="text-gray-400 text-center mt-3">
            {{ description }}
          </p>

          <div class="flex items-center justify-center gap-4 mt-8">
            <button
              @click="cancel"
              class="px-5 py-2 rounded-xl bg-white/10 text-gray-300 hover:bg-white/20 transition"
            >
              لغو
            </button>

            <button
              @click="confirm"
              :disabled="loading"
              class="flex items-center justify-center gap-2 px-5 py-2 rounded-xl bg-classic-gold text-black font-semibold min-w-[110px]"
            >
              <svg
                v-if="loading"
                class="w-5 h-5 animate-spin"
                viewBox="0 0 24 24"
                fill="none"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="black"
                  stroke-width="4"
                />
                <path
                  class="opacity-75"
                  fill="black"
                  d="M4 12a8 8 0 018-8v4l3-3-3-3v4a10 10 0 00-10 10h2z"
                />
              </svg>

              <span v-if="!loading">بله </span>
              <span v-else>در حال انجام</span>
            </button>
          </div>
        </div>
      </Transition>
    </div>
  </Transition>
</template>
<!-- Confirm Modal -->
<script setup lang="ts">
import { ref } from "vue"

const props = defineProps({
  modelValue: Boolean,
  title: { type: String, default: "آیا مطمئن هستید؟" },
  description: String,
})

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void
  (e: "confirm"): void
}>()

const loading = ref(false)

const cancel = () => {
  if (loading.value) return
  emit("update:modelValue", false)
}

const confirm = async () => {
  loading.value = true
  emit("confirm")
  loading.value = false
  emit("update:modelValue", false)
}
</script>

<style>
.overlay-enter-active,
.overlay-leave-active {
  transition: opacity 0.2s ease;
}
.overlay-enter-from,
.overlay-leave-to {
  opacity: 0;
}

.modal-enter-active {
  transition: all 0.25s ease;
}
.modal-leave-active {
  transition: all 0.2s ease;
}
.modal-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(10px);
}
.modal-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(10px);
}
</style>
