<template>
 <div :class="nested ? 'backdrop-blur-md bg-carb-gray/10 border border-classic-gold/30 rounded-xl p-4' : 'backdrop-blur-md bg-carb-gray/10 border border-white/10 rounded-2xl p-5 shadow-2xl'">
  <div class="flex justify-between items-center mb-3">

      <div class="flex items-center gap-3">
        <img :src="avatar" :alt="comment.user_name" class="w-12 h-12 rounded-full border border-classic-gold object-cover">

        <div>
          <p class="text-white text-sm">{{ comment.user_name }}</p>
      
          <span class="text-gray-400 text-xs">{{ toJalaliLong(comment.created_at) }}</span>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <button
          v-if="isOwner"
          type="button"
          :disabled="deleteLoading"
          @click="$emit('delete', comment.id)"
          class="text-gray-500 hover:text-rose-400 transition disabled:opacity-40 disabled:cursor-not-allowed"
          title="حذف نظر"
        >
          <Icon name="mdi:trash-can-outline" class="text-lg" />
        </button>

        <button
          type="button"
          @click="$emit('reply', comment.id)"
          class="text-gray-400 hover:text-classic-gold text-sm transition"
        >
          پاسخ
        </button>
      </div>

    </div>

    <p class="text-gray-300 leading-7 text-sm whitespace-pre-line">
      {{ comment.message }}
    </p>

    <div v-if="comment.replies?.length" class="mt-6 space-y-4 mr-10 border-r border-classic-gold/30 pr-6">
      <ProjectCommentItem
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        :current-username="currentUsername"
        nested
        @reply="$emit('reply', $event)"
        @delete="$emit('delete', $event)"
      />
    </div>

 </div> 
</template>

<script lang="ts" setup>
//  Comment item
import type { CommentDTO } from '~/models/Comment/SendCommentDTO'
import { toJalaliLong } from '~/utilities/dateHelpers'
import { resolveMediaUrl } from '~/utilities/urlHelpers'

const props = withDefaults(
  defineProps<{
    comment: CommentDTO
    nested?: boolean
    currentUsername?: string
    deleteLoading?: boolean
  }>(),
  {
    nested: false,
    currentUsername: '',
    deleteLoading: false,
  },
)

defineEmits<{
  reply: [number]
  delete: [number]
}>()

const avatar = computed(() => resolveMediaUrl(props.comment.user_avatar) || '/images/user1.jpg')
const isOwner = computed(() => !!props.currentUsername && props.comment.user_name === props.currentUsername)
</script>
