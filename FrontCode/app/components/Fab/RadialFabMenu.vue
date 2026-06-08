<template>

  <div class="fixed  z-50 left-4 bottom-4 md:left-6 md:bottom-6 select-none md:hidden">
    <div class="relative">
      <div
        v-show="visible"
        class="strip-shell bg-dark-gray/20 backdrop-blur-md  absolute top-1/2 z-0 left-[calc(3rem+10px)] md:left-[calc(3.5rem+10px)]
               h-12 md:h-14
               w-[clamp(180px,calc(100vw-112px),260px)]
               md:w-[clamp(240px,calc(100vw-120px),360px)]"
        :class="{
          'is-open': open && !closing,
          'is-closing': closing,
          'shadow-[0_20px_50px_rgba(0,0,0,0.45)]': open && !closing
        }"
        role="menu"
        aria-label="منوی کشویی"
        @animationend="onAnimEnd"
      >
        <div class="h-full w-full   text-white/90 shadow-2xl rounded-full overflow-hidden ">
          <div dir="ltr" class="h-full grid items-stretch gap-0 divide-x divide-white/10" :style="{ gridTemplateColumns: 'repeat(3, 1fr)' }">
           <FabItem @closewithanim="closeWithAnimFn" icon="mdi:post-outline" to="/" name="خانه"    />
     
           <FabItem @closewithanim="closeWithAnimFn" icon="mdi:earth" to="/" name="اکسپلور" />

           <FabItem @closewithanim="closeWithAnimFn" icon="mdi:home-outline" to="/" name="خانه" />
           
          </div>
        </div>
      </div>

      <button
        ref="triggerRef"
        class="relative z-10 w-12 h-12 md:w-14 md:h-14 grid place-items-center rounded-full text-white shadow-2xl cursor-pointer transition-colors duration-200 ease-[cubic-bezier(.2,.8,.2,1)] overflow-visible outline-none focus:outline-none"
        :class="open ? 'bg-classic-gold hover:bg-light-gold' : 'bg-deep-black hover:bg-black'"
        :aria-expanded="open ? 'true' : 'false'"
        :aria-label="open ? 'بستن منو' : 'باز کردن منو'"
        :disabled="animating"
        @click="toggle"
      >
        <span v-if="!open" class="pointer-events-none absolute inset-0 rounded-full ring-2 ring-classic-gold/70 animate-ping"></span>
        <span v-if="!open" class="pointer-events-none absolute inset-0 rounded-full ring-2 ring-classic-gold/40"></span>
        <BarsIcon v-if="!open" class="w-6 h-6" />
        <CloseIcon v-else class="w-6 h-6" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * - Ultra-sleek mobile-only Floating Action Button (FAB) navigation bar component.
 * - Drives responsive dynamic drawer ribbons engineered via high-performance clip-path keyframes.
 * - Implements strict structural layout isolations locked specifically below medium desktop viewports.
 */
import { ref, computed, h, resolveComponent, onBeforeUnmount } from 'vue'

const open = ref(false)
const visible = ref(false)
const closing = ref(false)
const animating = ref(false)
let openTimer: number | null = null
let closeTimer: number | null = null


function toggle() {
  if (animating.value) return
  if (!open.value) {
    visible.value = true
    closing.value = false
    animating.value = true
    requestAnimationFrame(() => { open.value = true })
    if (openTimer) clearTimeout(openTimer)
    openTimer = window.setTimeout(() => { animating.value = false }, 100)
  } else {
    closeWithAnimFn()
  }
}

function closeWithAnimFn() {
  if (!visible.value || animating.value) return
  closing.value = true
  open.value = false
  animating.value = true
  if (closeTimer) clearTimeout(closeTimer)
  closeTimer = window.setTimeout(() => {
    visible.value = false
    closing.value = false
    animating.value = false
  }, 700)
}

function onAnimEnd(e: AnimationEvent) {
  if (e.animationName === 'revealStrip') {
    if (openTimer) clearTimeout(openTimer)
    animating.value = false
    closing.value = false
  } else if (e.animationName === 'hideStrip') {
    if (closeTimer) clearTimeout(closeTimer)
    visible.value = false
    closing.value = false
    animating.value = false
  }
}

onBeforeUnmount(() => {
  if (openTimer) clearTimeout(openTimer)
  if (closeTimer) clearTimeout(closeTimer)
})

function BarsIcon(){ return h('svg',{xmlns:'http://www.w3.org/2000/svg',viewBox:'0 0 24 24'},[h('path',{fill:'currentColor',d:'M3 6h18v2H3zM3 11h18v2H3zM3 16h18v2H3z'})]) }
function CloseIcon(){ return h('svg',{xmlns:'http://www.w3.org/2000/svg',viewBox:'0 0 24 24'},[h('path',{d:'M6 6L18 18M18 6L6 18',stroke:'currentColor','stroke-width':'2.4','stroke-linecap':'round'})]) }

</script>

<style scoped>
.strip-shell {
  transform: translateY(-50%);
  will-change: clip-path, transform, opacity;
  clip-path: inset(0 100% 0 0 round 9999px);
}
.strip-shell.is-open { animation: revealStrip 420ms cubic-bezier(.16,.84,.24,1) forwards; }
.strip-shell.is-closing { animation: hideStrip 360ms cubic-bezier(.2,.8,.2,1) forwards; }

@keyframes revealStrip {
  from { clip-path: inset(0 100% 0 0 round 9999px); filter: blur(0.8px); opacity: .0; }
  60%  { filter: blur(0.25px); }
  to   { clip-path: inset(0 0 0 0 round 9999px); filter: blur(0); opacity: 1; }
}
@keyframes hideStrip {
  from { clip-path: inset(0 0 0 0 round 9999px); filter: blur(0); opacity: 1; }
  to   { clip-path: inset(0 100% 0 0 round 9999px); filter: blur(.35px); opacity: .98; }
}

.menu-item { opacity: 0; transform: translateY(6px) scale(.96); }
.is-open .menu-item { animation: itemIn 280ms cubic-bezier(.2,.8,.2,1) forwards; }
.is-open .menu-item:nth-child(1) { animation-delay: 80ms; }
.is-open .menu-item:nth-child(2) { animation-delay: 140ms; }
.is-open .menu-item:nth-child(3) { animation-delay: 200ms; }

.is-closing .menu-item { animation: itemOut 220ms cubic-bezier(.2,.8,.2,1) forwards; }
.is-closing .menu-item:nth-child(3) { animation-delay: 0ms; }
.is-closing .menu-item:nth-child(2) { animation-delay: 50ms; }
.is-closing .menu-item:nth-child(1) { animation-delay: 100ms; }

@keyframes itemIn  { to { opacity: 1; transform: translateY(0) scale(1); } }
@keyframes itemOut { to { opacity: 0; transform: translateY(6px) scale(.96); } }
</style>
