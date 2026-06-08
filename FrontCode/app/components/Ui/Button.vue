<template>
  <div v-if="variant === 'bracket'" :class="bracketWrapperClass">
    <component
      :is="componentType"
      :to="props.to || undefined"
      :type="props.to ? undefined : props.type"
      :disabled="props.disabled"
      :class="bracketInnerClass"
      v-bind="$attrs"
    >
      <span v-if="icon" class="text-lg ml-1 -mb-1 relative z-10 ">
        <Icon :name="icon" size="26"  />
      </span>
      <span class="relative z-10">
        <slot />
      </span>
    </component>
  </div>

  <component
    v-else
    :is="componentType"
    :to="props.to || undefined"
    :type="props.to ? undefined : props.type"
    :disabled="props.disabled"
    :class="wrapperClass"
    v-bind="$attrs"
  >
    <span v-if="icon" class="text-lg ml-1 -mb-1 relative z-10 ">
      <Icon :name="icon" size="26"  />
    </span>

    <span class="relative z-10">
      <slot />
    </span>

    <span
      v-if="variant === 'dark'"
      class="btn-slide absolute inset-0 bg-classic-gold translate-y-full transition-transform duration-300"
    ></span>

    <span
      v-if="variant === 'gold'"
      class="btn-shine absolute inset-0 pointer-events-none"
    ></span>
  </component>
</template>

<script setup lang="ts">

// User Interface Button component with multiple variants and optional icon support

import { computed, resolveComponent } from 'vue'
import type { RouteLocationRaw } from 'vue-router'

interface Props {
  variant?: 'gold' | 'dark' | 'outline' | 'simple' | 'bracket' 
  type?: 'button' | 'submit'
  to?: RouteLocationRaw | null
  full?: boolean
  disabled?: boolean
  icon?: string | null
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'gold',
  type: 'button',
  to: null,
  full: false,
  disabled: false,
  icon: null
})

const componentType = computed(() => {
  return props.to ? resolveComponent('NuxtLink') : 'button'
})

const bracketWrapperClass = computed(() => {
  const base = 'group border-x-2 border-light-gold rounded-full p-[3px] transition-all duration-300 ease-out hover:p-[6px] hover:scale-95'
  const width = props.full ? 'flex w-full justify-center' : 'inline-flex'
  const disabledClass = props.disabled ? 'opacity-60 cursor-not-allowed pointer-events-none' : 'cursor-pointer'
  
  return `${base} ${width} ${disabledClass}`
})

const bracketInnerClass = computed(() => {
  const base = 'bg-classic-gold text-deep-black font-bold py-2 px-8 rounded-full transition-all duration-300 text-lg shadow-md group-hover:shadow-lg group-hover:bg-light-gold flex items-center justify-center'
  const width = props.full ? 'w-full' : ''
  
  return `${base} ${width}`
})


const variantClass = computed(() => {
  if (props.disabled) {
    return 'bg-dark-gray text-gray-500 opacity-60'
  }

  switch (props.variant) {
    case 'gold':
      return 'bg-classic-gold text-deep-black shadow-lg shadow-classic-gold/20'
    case 'dark':
      return 'bg-dark-gray text-bone-white hover:text-deep-black'
    case 'outline':
      return 'border border-classic-gold text-classic-gold bg-transparent hover:bg-classic-gold hover:text-deep-black'
    case 'simple':
      return 'bg-gray-200 text-gray-800 hover:bg-gray-300'
    default:
      return ''
  }
})

const wrapperClass = computed(() => {
  const base = `
    group
    relative
    flex items-center justify-center
    overflow-hidden
    rounded-lg
    font-semibold
    transition-all
    duration-300
    px-6 py-3
  `

  const width = props.full ? 'w-full' : 'inline-flex'

  if (props.disabled) {
    return `
      ${base}
      ${width}
      ${variantClass.value}
      cursor-not-allowed
      text-white
      pointer-events-none
      opacity-60
    `
  }

  const scale =
    props.variant === 'simple'
      ? 'active:scale-95'
      : 'hover:scale-105'

  return `
    ${base}
    ${width}
    ${variantClass.value}
    ${scale}
    cursor-pointer
  `
})
</script>

<style scoped>
.group:hover .btn-slide {
  transform: translateY(0);
}

.btn-shine::before {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.5),
    transparent
  );
  transition: 0.5s;
}

.group:hover .btn-shine::before {
  left: 150%;
}
</style>
