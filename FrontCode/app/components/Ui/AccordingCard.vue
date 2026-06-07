<template>
  <div class="backdrop-blur-md shadow-2xl bg-carb-gray/10 border border-white/10 hover:border-light-gold hover:shadow-light-gold/20 transition rounded-2xl">

   
    <button
      @click="open = !open"
      class="w-full flex items-center  relative justify-between p-6 text-right"
    >
      <div class="flex items-center gap-3 ">
        <Icon name="mdi:chevron-down"
          class="transition-transform duration-300 absolute left-5 top-5"
          :class="open ? 'rotate-180 text-light-gold' : 'text-gray-400'"
          size="24"
        />

        <span class="text-bone-white font-medium">
         {{ props.title }}
        </span>
      </div>
    </button>

    <transition
      enter-active-class="transition-all duration-300 ease-out"
      leave-active-class="transition-all duration-200 ease-in"
      enter-from-class="opacity-0 max-h-0"
      enter-to-class="opacity-100 max-h-[700px]"
      leave-from-class="opacity-100 max-h-[700px]"
      leave-to-class="opacity-0 max-h-0"
    >
      <div v-show="open" class="px-6 pb-6 overflow-hidden">
        <slot />
      </div>
    </transition>

  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"

const open = ref(false)
const props = defineProps({
    title:{
        type:String,
        default:'عنوان کارت'
    },
    isOpen:{
      type:Boolean,
      default:false
    }
})
onMounted(()=>{

open.value=props.isOpen
})


</script>
