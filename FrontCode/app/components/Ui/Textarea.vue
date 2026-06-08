<template>
   <div class="space-y-1">
            <label :for="name+'id'" class="block text-sm font-medium mb-2 text-bone-white">{{ label }}</label>
            <textarea 
              :id="name+'id'"
              :rows="rows"
              :value="modelValue"
              @input="handle"
              :disabled="disabled"
              :placeholder="placeholder"
              :class="['w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-1 focus:ring-classic-gold focus:border-classic-gold outline-none transition-all dir-ltr text-left',
              { 'border-red-600': errorMessage },
               { 'cursor-not-allowed': disabled },
               {'text-right':rtl}
        ]"
            ></textarea>
            <span v-if="!ignoreErrorMessage && errorMessage" class="text-error mt-2 py-2  ">
              {{errorMessage}}
              </span>
          </div>
</template>

<script lang="ts" setup>
// Input component integrated with vee-validate for form validation and 
// error handling, supporting various input types, RTL text, and customizable labels and placeholders
import {useField} from 'vee-validate'

const props=defineProps({

  name:{
    type:String,
    required:true,
  },
  rtl:{
    type:Boolean,
    default:false
  },

  label:{
    type:String,
    default:'text'
  },
  rows:{
    type:Number,
    default:5
  },
  disabled:{
    type:Boolean,
    default:false
  },
  placeholder:{
    type:String,
    default:''
  },
  ignoreErrorMessage: { 
      type: Boolean, 
      default: false 
  },
  modelValue: {
     default: '' 
    },


})
const {errorMessage,value,handleChange,setValue}=useField(props.name,undefined,{
  initialValue:props.modelValue
})
watch(() => props.modelValue, (val) => setValue(val))
const emit = defineEmits(['update:modelValue'])

const handle = (e: any) => {
  emit('update:modelValue', e.target.value)
  handleChange(e)
}
</script>

<style>

</style>
