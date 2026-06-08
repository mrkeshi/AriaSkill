<template>
  <Transition name="overlay">
    <div
      v-if="modelValue"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
    >
      <Transition name="modal">
        <div
          v-if="modelValue"
          class="w-full max-w-xl mx-4 rounded-2xl border border-white/10 bg-black/60 backdrop-blur-xl p-8 shadow-xl"
          dir="rtl"
        >
          <div class="mb-6 border-b border-white/10 pb-4">
            <h3 class="text-classic-gold font-bold text-lg">
              {{ author }}
            </h3>

            <p class="text-gray-300 mt-2 leading-7">
              {{ comment }}
            </p>
          </div>

          <div class="space-y-4">
            <UiTextarea
              name="reply"
              label="پاسخ شما"
              placeholder="پاسخ خود را بنویسید..."
              v-model="reply"
              rtl
            />

            <div class="flex justify-end gap-3">
              <button
                @click="cancel"
                class="px-5 py-2 rounded-xl bg-white/10 text-gray-300 hover:bg-white/20 transition"
              >
                لغو
              </button>

              <UiButton
                variant="gold"
                :disabled="loading || !reply"
                @click="submit"
              >
                <span v-if="!loading">ثبت پاسخ</span>
                <span v-else>در حال ارسال...</span>
              </UiButton>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </Transition>
</template>

<script setup>
/**
 * ReplyModal Component
 * 
 * A reusable modal dialog that allows users to write and submit a reply 
 * to a specific comment. Features a blurred backdrop backdrop, smooth entry/exit 
 * transitions, RTL support, and handles loading states during submission.
 * 
 * @props {Boolean} modelValue - Controls the visibility of the modal (v-model).
 * @props {String} author - The name of the original comment's author.
 * @props {String} comment - The text content of the original comment being replied to.
 * @props {Function} onSubmit - Async callback function triggered when the reply is submitted.
 * 
 * @emits update:modelValue - Emitted to sync the modal's visibility state with the parent.
 */

import { ref } from "vue"

const props = defineProps({
  modelValue: Boolean,
  author: String,
  comment: String,
  onSubmit: { type: Function, required: true }
})

const emit = defineEmits(["update:modelValue"])

const loading = ref(false)
const reply = ref("")

const cancel = () => {
  if (loading.value) return
  emit("update:modelValue", false)
}

const submit = async () => {
  if (!reply.value) return

  loading.value = true
  await props.onSubmit(reply.value)
  loading.value = false

  reply.value = ""
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
