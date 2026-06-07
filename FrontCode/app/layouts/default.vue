<template>
  <div>
    <header-the-header></header-the-header>
    <fab-radial-fab-menu></fab-radial-fab-menu>
      <div class="bg-deep-black min-h-screen text-bone-white">
    <main class=" container mx-auto px-6 md:px-8 pb-10">
    <slot />
    </main>
    </div>
  <div class="neon-background">
  <div class="neon-layer"></div>
  <div class="neon-layer"></div>
</div>
<FooterTheFooter></FooterTheFooter>

  </div>
  
</template>

<script lang="ts" setup>


</script>

<style>

</style>