<!-- Dashboard Layout -->
<template>
  <div
    class="min-h-screen grid "
    :style="{
      gridTemplateColumns: sidebarWidth + ' 1fr',
      gridTemplateRows: '80px 1fr'
    }"
  >
    <DashboardSidebar
      class="row-span-2 "
      :collapsed="collapsed"
         @toggle="collapsed = !collapsed"
    />

    <DashboardHeader
    />
    <main class="lg:p-8 lg:py-12 overflow-y-auto bg-transparent">
      <slot />
    </main>
  </div>
</template>

<script setup>
const collapsed = ref(false)

const sidebarWidth = computed(() =>
  collapsed.value ? '80px' : '288px'
)
</script>


<style>
body {
  background-image: url('/images/dash-background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

</style>