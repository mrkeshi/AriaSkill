<template>
  <!--
    This component intentionally has no extra markup.
    The .client.vue suffix makes Nuxt skip SSR for this subtree entirely,
    so <apexchart> is never evaluated on the server.
    All props/attrs are forwarded to <apexchart> via v-bind="$attrs".
  -->
  <apexchart v-bind="$attrs" />
</template>

<script setup lang="ts">
// Disable attribute inheritance on the wrapper so $attrs flows through cleanly.
defineOptions({ inheritAttrs: false })
</script>
