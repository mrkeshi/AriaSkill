<template>
  <ui-card-blury>
    <h3 class="text-white font-semibold mb-4">درباره سازنده</h3>

    <div class="flex items-center gap-4">
      <img 
        v-if="user.avatar" 
        :src="avatar" 
        :alt="user.full_name" 
        class="w-14 h-14 rounded-full border-2 border-classic-gold object-cover"
      />
      
      <div 
        v-else 
        class="w-14 h-14 rounded-full border-2 border-classic-gold bg-zinc-800 text-white flex items-center justify-center font-bold text-lg uppercase"
      >
        {{ userInitial }}
      </div>

      <div>
        <p class="text-white">{{ user.full_name || user.username }}</p>
        <span class="text-gray-400 text-sm">@{{ user.username }}</span>
      </div>
    </div>

    <div class="mt-5">
      <UiButton
        variant="outline"
        full
        :to="`/@${user.username}`"
      >
        مشاهده پروفایل
      </UiButton>
    </div>
  </ui-card-blury>
</template>

<script lang="ts" setup>

/**
 * - Implements a highly cohesive avatar profile teaser card component.
 * - Bridges layout state computations for dynamic static media route resolutions.
 * - Handles safe string fallbacks utilizing deterministic initial character scrapers.
 */

import type { UserSummaryDTO } from '~/models/User/UserDTO'
import { resolveMediaUrl } from '~/utilities/urlHelpers'
import { userInitialFrom } from '~/utilities/stringHelpers'

const props = defineProps<{ user: UserSummaryDTO }>()
const avatar = computed(() => resolveMediaUrl(props.user.avatar))
const userInitial = computed(() => userInitialFrom(props.user))
</script>