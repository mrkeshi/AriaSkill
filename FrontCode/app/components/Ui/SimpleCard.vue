<template>
  <div class="min-h-screen flex items-center justify-center p-6 max-md:p-4" dir="rtl">
    <div class="bg-dark-gray/20 login-card w-full max-w-md rounded-2xl shadow-xl overflow-hidden">
      <div class="p-10 max-md:p-8 flex flex-col items-center text-center space-y-6">
        <div class="w-20 h-20  bg-classic-gold/10 rounded-full flex items-center justify-center mb-3">
         <Icon :name="icon" class="text-4xl text-classic-gold" />
        </div>
        <div class="space-y-3 w-full">
          <h1 class="text-2xl font-bold text-classic-gold">{{ title }}</h1>
          <p class="text-sm text-bone-white leading-relaxed">
         {{ description }}
          </p>
        </div>

        <div class="w-full pt-4" v-if="to">
         <UiButton :to="{ name: to }" variant="gold" full class="text-md">
      {{ toName }}
         </UiButton>
        </div>

      </div>


    </div>
  </div>
</template>

<script setup lang="ts">



const props=defineProps({
  icon:{
    type:String,
    default:''
  },
   title:{
    type:String,
    required:true
  },
    description:{
    type:String,
    required:true
  },
  to:{
    required:false,
    type:String,

  },
  toName:{
    required:false,
    type:String
  }
})



</script>
<style></style>