<template>

<div>


 <NuxtLoadingIndicator color="#d4af37" :height="5" :throttle="0" />

   <nuxt-layout>
    <NuxtPage />
   </nuxt-layout>
     
</div>


</template>
<script lang="ts" setup>
useHead({
  link: [
    { rel: 'icon', type: 'image/png', href: '/images/favIcon.ico.png' },
    { rel: 'shortcut icon', href: '/images/favIcon.ico.png' }
  ]
})
</script>
