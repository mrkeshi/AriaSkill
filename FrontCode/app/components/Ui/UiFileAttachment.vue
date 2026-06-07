<template>
  <div class="space-y-2">

    <label v-if="label" :for="name" class="text-sm font-medium text-gray-300 ml-1">
      {{ label }}
    </label>
    
    <div 
      @click="triggerInput"
      class="relative flex items-center justify-between bg-white/5 border rounded-xl px-4 py-3 transition-all cursor-pointer group overflow-hidden shadow-inner"
      :class="[
        errorMessage 
          ? 'border-rose-500/50 bg-rose-500/5 hover:bg-rose-500/10' 
          : 'border-white/10 hover:bg-white/10 hover:border-classic-gold/30'
      ]"
    >

      <input 
        ref="fileInputRef"
        :id="name"
        type="file" 
        class="hidden" 
        :accept="accept"
        @change="handleFileUpload" 
      >
      
      <div class="flex items-center gap-3 overflow-hidden w-full">
        <div 
          class="p-2 rounded-lg transition-colors flex-shrink-0 flex items-center justify-center"
          :class="selectedFile ? 'bg-classic-gold/10 text-classic-gold' : 'bg-white/5 text-gray-400 group-hover:text-classic-gold'"
        >
           <Icon :name="selectedFile ? 'mdi:folder-zip-outline' : 'mdi:paperclip'" class="text-2xl" />
        </div>

        <div class="flex flex-col overflow-hidden w-full">
           <span v-if="selectedFile" class="text-white text-sm truncate dir-ltr text-left" dir="ltr">
             {{ selectedFile.name }}
           </span>
           <span v-else class="text-gray-500 text-sm truncate">
             {{ placeholder || 'انتخاب فایل ضمیمه...' }}
           </span>
           <span v-if="selectedFile" class="text-xs text-gray-400 mt-0.5 dir-ltr text-left font-sans">
             {{ formatFileSize(selectedFile.size) }}
           </span>
        </div>
      </div>
      <button 
        v-if="selectedFile" 
        @click.stop="clearFile" 
        class="p-1.5 text-gray-400 hover:text-rose-400 hover:bg-rose-400/10 rounded-lg transition-colors flex-shrink-0 mr-2"
        title="حذف فایل"
      >
        <Icon name="mdi:close" class="text-lg" />
      </button>
      <Icon v-else name="mdi:cloud-upload-outline" class="text-gray-400 group-hover:text-classic-gold transition-colors flex-shrink-0 mr-2 text-xl" />
    </div>

    <p v-if="errorMessage" class="text-xs text-rose-400 mt-1 flex items-center gap-1">
      <Icon name="mdi:alert-circle-outline" class="text-sm" />
      {{ errorMessage }}
    </p>
    <p v-else-if="hint" class="text-xs text-gray-500 mt-1">
      {{ hint }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useField } from 'vee-validate'

const props = defineProps({
  name: { type: String, required: true },
  label: { type: String, default: '' },
  accept: { type: String, default: '.zip,.rar,.tar.gz,.pdf' },
  placeholder: { type: String, default: '' },
  hint: { type: String, default: '' },
  modelValue: { type: File, default: null }
})

const emit = defineEmits(['update:modelValue'])

const fileInputRef = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(props.modelValue || null)

const { value, errorMessage, handleChange } = useField<File | null>(() => props.name)

const triggerInput = () => {
  fileInputRef.value?.click()
}

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0] || null
  
  if (file) {
    selectedFile.value = file
    handleChange(file)
    emit('update:modelValue', file)
  }
}
const clearFile = () => {
  selectedFile.value = null
  handleChange(null)
  emit('update:modelValue', null)
  if (fileInputRef.value) {
    fileInputRef.value.value = '' 
  }
}
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}


watch(() => props.modelValue, (newVal) => {
  if (newVal !== selectedFile.value) {
    selectedFile.value = newVal
    handleChange(newVal)
  }
})
</script>
