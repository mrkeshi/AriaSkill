<template>

         <NuxtLink
              :to="to"
              class="menu-item px-3 md:px-5 flex items-center justify-center hover:bg-classic-gold active:bg-light-gold hover:text-white active:text-white transition-transform duration-300 ease-[cubic-bezier(.2,.8,.2,1)]"
              role="menuitem" :aria-label="name" @click="emit('closewithanim')"
            >
              <span class="sr-only" v-text="name"></span>
            <Icon :name="icon" class="text-2xl text-white opacity-95" />
     
          </NuxtLink>

</template>

<script lang="ts" setup>

const emit=defineEmits(["closewithanim"])

const props=defineProps({
  name:{type:String,default:'منو'},
  to:{type:String,default:'/'},
  icon:{type:String,default:'home'},
})
</script>

<style>

</style>