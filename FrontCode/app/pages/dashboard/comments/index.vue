<template>
  <UiCardBlury>
    <div
      v-if="replyModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
      @click.self="closeReplyModal"
    >
      <div class="bg-slate-900 border border-white/10 rounded-2xl p-6 w-full max-w-lg shadow-2xl" dir="rtl">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-white font-bold text-base">پاسخ به نظر</h3>
          <button type="button" class="text-gray-400 hover:text-white transition" @click="closeReplyModal">
            <Icon name="mdi:close" class="text-xl" />
          </button>
        </div>
        <div class="mb-4 p-3 rounded-xl bg-white/[0.03] border border-white/10 text-gray-400 text-sm leading-relaxed line-clamp-3">
          {{ selectedComment?.message }}
        </div>
        <Form @submit="submitReply" :validation-schema="ReplySchema" class="space-y-4">
          <UiTextarea
            rtl
            name="replyMessage"
            v-model="replyForm.message"
            label="متن پاسخ"
            placeholder="پاسخ خود را بنویسید..."
            :disabled="replyLoading"
          />
          <div class="flex justify-end gap-3">
            <button
              type="button"
              class="px-4 py-2 rounded-lg border border-white/10 text-gray-400 hover:text-white transition text-sm"
              @click="closeReplyModal"
            >
              انصراف
            </button>
            <UiButton type="submit" variant="bracket" :disabled="replyLoading">
              {{ replyLoading ? 'در حال ارسال...' : 'ارسال پاسخ' }}
            </UiButton>
          </div>
        </Form>
      </div>
    </div>

    <div class="space-y-6" dir="rtl">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <h2 class="text-xl font-bold text-white tracking-wide">
          نظرات دریافتی
          <span class="bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-3 py-1 rounded-full text-xs mr-2">
            {{ toPersianNumerals(totalCount) }} نظر
          </span>
        </h2>
      </div>

      <SkeletonSimple v-if="pending" :repeat="5" class="h-16 mb-2" />

      <div v-else class="overflow-x-auto rounded-2xl border border-white/10 bg-white/[0.03] backdrop-blur-xl shadow-2xl">
        <table class="w-full text-right whitespace-nowrap border-collapse">
          <thead class="bg-white/[0.04] text-gray-400 text-xs font-bold uppercase tracking-wider border-b border-white/10">
            <tr>
              <th class="p-4 text-center w-12">#</th>
              <th class="p-4">کاربر</th>
              <th class="p-4">پروژه</th>
              <th class="p-4">تاریخ</th>
              <th class="p-4">پیام</th>
              <th class="p-4 text-center">وضعیت</th>
              <th class="p-4 text-center">عملیات</th>
            </tr>
          </thead>

          <tbody class="text-gray-200 text-sm divide-y divide-white/[0.06]">
            <tr
              v-for="(item, index) in comments"
              :key="item.id"
              class="hover:bg-white/[0.05] transition-all duration-300 group"
              :class="{ 'opacity-50': item.status === 'inactive' }"
            >
              <td class="p-4 text-center text-gray-500 font-mono text-xs">{{ toPersianNumerals(rowNumber(index, currentPage.value, 10)) }}</td>

              <td class="p-4">
                <div class="flex items-center gap-3">
                  <img
                    v-if="item.user_avatar"
                    :src="resolveMediaUrl(item.user_avatar)"
                    :alt="item.user_name"
                    class="w-10 h-10 rounded-full object-cover border border-white/20 shadow-lg"
                  >
                  <div
                    v-else
                    class="w-10 h-10 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-300 flex items-center justify-center font-bold text-base shadow-lg"
                  >
                    {{ firstLetter(item.user_name) }}
                  </div>
                  <div class="flex flex-col">
                    <span class="font-medium text-white">{{ item.user_name }}</span>
                    <span class="text-gray-500 text-xs">#{{ toPersianNumerals(item.user) }}</span>
                  </div>
                </div>
              </td>

              <td class="p-4">
                <NuxtLink
                  :to="`/projects/pr-${item.project_slug}`"
                  class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-lg bg-classic-gold/10 text-classic-gold border border-classic-gold/20 hover:bg-classic-gold/20 transition"
                  :title="`مشاهده پروژه: ${item.project_title}`"
                >
                  <Icon name="mdi:open-in-new" class="text-xs" />
                  {{ item.project_title }}
                </NuxtLink>
              </td>

              <td class="p-4 text-gray-400 text-xs">{{ toJalaliLong(item.created_at) }}</td>

              <td class="p-4 text-gray-300 max-w-xs truncate" :title="item.message">{{ item.message }}</td>

              <td class="p-4 text-center">
                <span
                  class="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-full border"
                  :class="item.status === 'active'
                    ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
                    : 'bg-rose-500/10 text-rose-300 border-rose-500/30'"
                >
                  <span class="w-1.5 h-1.5 rounded-full" :class="item.status === 'active' ? 'bg-emerald-400' : 'bg-rose-400'"></span>
                  {{ item.status === 'active' ? 'فعال' : 'غیرفعال' }}
                </span>
              </td>

              <td class="p-4">
                <div class="flex items-center justify-center gap-2">
                  <button
                    type="button"
                    title="پاسخ"
                    class="bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 p-2 rounded-lg flex items-center justify-center text-cyan-400 hover:text-cyan-300 transition"
                    @click="openReply(item)"
                  >
                    <Icon name="mdi:reply-outline" class="text-lg" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="comments.length === 0" class="p-12 text-center text-gray-500 flex flex-col items-center justify-center gap-2">
          <Icon name="mdi:comment-off-outline" class="text-4xl text-gray-600" />
          <span class="text-sm font-medium">هنوز نظری برای پروژه‌های شما ثبت نشده است.</span>
        </div>
      </div>

      <UiPagination :totalPages="totalPages" />
    </div>
  </UiCardBlury>
</template>

<script setup lang="ts">
import { object, string } from 'yup'
import { Form } from 'vee-validate'
import type { CommentManagementDTO } from '~/models/Comment/SendCommentDTO'
import {
  getMyProjectCommentsService,
  sendProjectCommentService,
} from '~/services/projects/project.Service'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { generateSeoMeta } from '~/utilities/seo'
import { toJalaliLong, toPersianNumerals } from '~/utilities/dateHelpers'
import { resolveMediaUrl } from '~/utilities/urlHelpers'
import { firstLetter, rowNumber } from '~/utilities/stringHelpers'
import { useCurrentPage } from '~/composable/useCurrentPage'

definePageMeta({ layout: 'dashboard' })

const ReplySchema = object({
  replyMessage: string().required('متن پاسخ الزامی است').min(3, 'پاسخ باید حداقل ۳ کاراکتر داشته باشد'),
})

const route = useRoute()
const { currentPage } = useCurrentPage()
const { showSuccess } = useCustomToastify()

const replyModal = ref(false)
const selectedComment = ref<CommentManagementDTO | null>(null)
const replyForm = reactive({ message: '' })
const replyLoading = ref(false)

const openReply = (item: CommentManagementDTO) => {
  selectedComment.value = item
  replyForm.message = ''
  replyModal.value = true
}

const closeReplyModal = () => {
  replyModal.value = false
  selectedComment.value = null
  replyForm.message = ''
}

const submitReply = async (_: unknown, { resetForm }: any) => {
  if (!selectedComment.value || replyLoading.value) return
  replyLoading.value = true
  try {
    await sendProjectCommentService(selectedComment.value.project, {
      message: replyForm.message,
      parent: selectedComment.value.id,
    })
    showSuccess({ title: 'پاسخ ارسال شد', message: 'پاسخ شما با موفقیت ثبت شد.' })
    resetForm()
    closeReplyModal()
    await refresh()
  } finally {
    replyLoading.value = false
  }
}

const { data, refresh, pending } = await useAsyncData(
  'my-project-comments',
  () => getMyProjectCommentsService(currentPage.value),
  { watch: [currentPage] },
)

const comments = computed<CommentManagementDTO[]>(() => data.value?.data?.results ?? [])
const totalCount = computed(() => data.value?.data?.count ?? 0)
const totalPages = computed(() => Math.ceil(totalCount.value / 10))

useHead(generateSeoMeta({
  title: 'نظرات دریافتی',
  description: 'مشاهده نظرهای ثبت شده برای پروژه‌های من',
  image: '',
  url: '',
  keywords: ['نظرات', 'پروژه'],
  author: 'AriaSkill',
  type: 'website',
}))
</script>
