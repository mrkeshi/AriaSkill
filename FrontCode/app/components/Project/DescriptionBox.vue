<template>
<ui-card-blury>
        <h2 class="text-xl font-semibold text-white mb-4">توضیحات پروژه</h2>

        <p class="text-gray-300 leading-8  text-justify">
          {{ description }}
        </p>
     </ui-card-blury>
</template>

<script lang="ts" setup>
defineProps<{ description: string }>()
</script>
