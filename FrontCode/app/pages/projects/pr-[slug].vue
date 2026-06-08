<template>
  <div class="container mx-auto px-4 py-10" dir="rtl">
    <Confirm
      v-model="deleteCommentModal"
      title="حذف نظر"
      description="آیا مطمئن هستید که می‌خواهید این نظر را حذف کنید؟"
      @confirm="confirmDeleteComment"
    />

    <SkeletonSimple v-if="pending" :repeat="6" class="h-24 mb-4" />

    <div v-else-if="notFound" class="max-w-2xl mx-auto text-center py-20">
      <Icon name="mdi:file-search-outline" class="text-6xl text-classic-gold mb-4" />
      <h1 class="text-2xl font-bold text-white mb-3">پروژه پیدا نشد</h1>
      <p class="text-gray-400 mb-6">ممکن است این پروژه حذف شده باشد یا هنوز برای نمایش عمومی آماده نباشد.</p>
      <UiButton variant="outline" to="/projects/filter">بازگشت به پروژه‌ها</UiButton>
    </div>

    <div v-else-if="project" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <main class="space-y-6 lg:col-span-2">
        <div class="backdrop-blur-md shadow-2xl bg-carb-gray/10 hover:shadow-classic-gold/30 border-white/10 transition hover:border-light-gold border-2 rounded-2xl overflow-hidden">
          <img :src="projectImage" :alt="project.title" class="w-full h-[420px] object-cover" />
        </div>

        <ProjectDetailBox :project="project" />
        <ProjectDescriptionBox :description="project.description" />
        <ProjectShareLikeBox
          :project="project"
          :loading="likeLoading"
          @toggle-like="toggleLike"
          @share="shareProject"
        />

        <div class="space-y-8">
          <ProjectSendComment
            :parent-id="replyParentId"
            :loading="commentLoading"
            :title="commentFormTitle"
            @submit="submitComment"
          />

          <div v-if="replyParentId" class="flex justify-end -mt-6">
            <button type="button" class="text-sm text-gray-400 hover:text-classic-gold transition" @click="replyParentId = null">
              لغو پاسخ
            </button>
          </div>

          <SkeletonSimple v-if="commentsPending" :repeat="3" class="h-20 mb-3" />

          <div v-else-if="comments.length" class="space-y-5">
            <ProjectCommentItem
              v-for="comment in comments"
              :key="comment.id"
              :comment="comment"
              :current-username="authStore.user.username"
              :delete-loading="deletingCommentId === comment.id"
              @reply="setReply"
              @delete="openDeleteComment"
            />
          </div>

          <UiCardBlury v-else>
            <p class="text-center text-gray-400">هنوز نظری برای این پروژه ثبت نشده است. اولین نظر را شما بنویسید.</p>
          </UiCardBlury>
        </div>
      </main>

      <aside class="space-y-6 lg:col-span-1">
        <ProjectAuthorBox :user="project.user" />
        <ProjectDownloadBox
          :project="project"
          :loading="downloadLoading"
          @download="downloadProject"
        />
        <ProjectSkillBox :skills="project.skills" />
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * @module ProjectPublicProfileController
 * @description Core interactive hub managing public project presentation, interactive social actions, 
 * and conversational comment threads on the Aria Craft (آریا کرفت) platform.
 * 
 * @architectural_patterns
 * - Top-Level Await (SSR): Executes sequential blocking asynchronous calls (`loadProject` -> `loadComments`) 
 *   during Nuxt's server-side rendering phase to ensure HTML metadata and initial lists are pre-hydrated for crawlers.
 * - Reactive Route Tracking: Binds an active `watch` closure to dynamic URL slug variations to reset context states 
 *   and re-trigger page fetch logic smoothly during nested view shifts.
 * - Defensive Normalization: Implements an inline structural morph (`normalizeComments`) to safely map varying REST 
 *   payload envelopes (both raw array feeds and paginated result blocks) down into predictable local arrays.
 * 
 * @platform_and_security_guards
 * - Intent Interception: Wraps destructive or high-privilege social vectors (liking, downloading, commenting) 
 *   behind stateful auth barriers (`ensureAuthenticated`) to prevent unauthenticated server strain.
 * - Web API Isolation: Wraps client-centric features—such as asynchronous window redirection (`window.open`), 
 *   native device sheets (`navigator.share`), and pasteboard interaction (`navigator.clipboard`) — within explicit 
 *   `import.meta.client` evaluation sandboxes to protect Node.js context boundaries.
 */
import type { CommentDTO } from '~/models/Comment/SendCommentDTO'
import type { ProjectDTO } from '~/models/Project/ProjectDTO'
import {
  deleteCommentService,
  downloadProjectService,
  getProjectCommentsService,
  likeProjectService,
  retrieveProjectService,
  sendProjectCommentService,
  unlikeProjectService,
} from '~/services/projects/project.Service'
import { useAuthRequiredAction } from '~/composable/useAuthRequiredAction'
import { useCustomToastify } from '~/composable/useCustomToasitify'
import { generateSeoMeta } from '~/utilities/seo'
import { resolveMediaUrl } from '~/utilities/urlHelpers'

const route = useRoute()
const requestUrl = useRequestURL()
const slug = computed(() => String(route.params.slug || ''))
const { ensureAuthenticated } = useAuthRequiredAction()
const { showInfo, showSuccess } = useCustomToastify()
const authStore = useAuthStore()

const project = ref<ProjectDTO | null>(null)
const comments = ref<CommentDTO[]>([])
const pending = ref(true)
const commentsPending = ref(false)
const likeLoading = ref(false)
const downloadLoading = ref(false)
const commentLoading = ref(false)
const notFound = ref(false)
const replyParentId = ref<number | null>(null)

const deleteCommentModal = ref(false)
const selectedCommentId = ref<number | null>(null)
const deletingCommentId = ref<number | null>(null)

const projectImage = computed(() => resolveMediaUrl(project.value?.image) || '/images/project-1.jpg')
const commentFormTitle = computed(() => replyParentId.value ? 'ثبت پاسخ' : 'ثبت نظر')

const setProject = (data: ProjectDTO) => {
  project.value = data
}

const loadProject = async () => {
  pending.value = true
  notFound.value = false

  try {
    const res = await retrieveProjectService(slug.value)
    setProject(res.data)
  } catch (e) {
    project.value = null
    notFound.value = true
  } finally {
    pending.value = false
  }
}

const normalizeComments = (data: any): CommentDTO[] => Array.isArray(data) ? data : data?.results ?? []

const loadComments = async () => {
  if (!project.value?.id) return

  commentsPending.value = true
  try {
    const res = await getProjectCommentsService(project.value.id)
    comments.value = normalizeComments(res.data)
  } finally {
    commentsPending.value = false
  }
}

await loadProject()
await loadComments()

watch(slug, async () => {
  await loadProject()
  await loadComments()
})

const toggleLike = async () => {
  if (!project.value || likeLoading.value) return
  if (!ensureAuthenticated('برای پسندیدن پروژه باید وارد حساب کاربری خود شوید.')) return

  likeLoading.value = true
  try {
    const service = project.value.user_has_liked ? unlikeProjectService : likeProjectService
    const res = await service(project.value.slug)
    project.value.likes_count = res.data.likes_count
    project.value.user_has_liked = res.data.liked
  } catch (e) {
    showInfo({
      title: 'وضعیت پسندیدن',
      message: 'وضعیت پسندیدن پروژه به‌روزرسانی شد. لطفا دوباره بررسی کنید.',
    })
    await loadProject()
  } finally {
    likeLoading.value = false
  }
}

const downloadProject = async () => {
  if (!project.value || downloadLoading.value) return
  if (!ensureAuthenticated('برای دانلود پروژه باید وارد حساب کاربری خود شوید.')) return

  if (!project.value.file) {
    showInfo({
      title: 'فایل پروژه موجود نیست',
      message: 'برای این پروژه هنوز فایلی ثبت نشده است.',
    })
    return
  }

  downloadLoading.value = true
  try {
    const res = await downloadProjectService(project.value.slug)
    project.value.download_count = res.data.download_count

    if (import.meta.client) {
      window.open(resolveMediaUrl(project.value.file), '_blank', 'noopener,noreferrer')
    }
  } finally {
    downloadLoading.value = false
  }
}

const submitComment = async (
  payload: { message: string; parent: number | null },
  resetForm: () => void,
) => {
  if (!project.value || commentLoading.value) return
  if (!ensureAuthenticated('برای ثبت نظر باید وارد حساب کاربری خود شوید.')) return

  commentLoading.value = true
  try {
    await sendProjectCommentService(project.value.id, payload)
    resetForm()
    replyParentId.value = null
    showSuccess({
      title: 'نظر شما ثبت شد',
      message: 'نظر شما با موفقیت ارسال شد و پس از تایید نمایش داده می‌شود.',
    })
    await loadComments()
    await loadProject()
  } finally {
    commentLoading.value = false
  }
}

const setReply = (commentId: number) => {
  if (!ensureAuthenticated('برای پاسخ دادن به نظرها باید وارد حساب کاربری خود شوید.')) return
  replyParentId.value = commentId
}

const openDeleteComment = (commentId: number) => {
  selectedCommentId.value = commentId
  deleteCommentModal.value = true
}

const confirmDeleteComment = async () => {
  if (!selectedCommentId.value) return
  deletingCommentId.value = selectedCommentId.value
  try {
    await deleteCommentService(selectedCommentId.value)
    showSuccess({
      title: 'نظر حذف شد',
      message: 'نظر شما با موفقیت حذف شد.',
    })
    selectedCommentId.value = null
    await loadComments()
    await loadProject()
  } finally {
    deletingCommentId.value = null
  }
}

const shareProject = async () => {
  const url = `${requestUrl.origin}${route.fullPath}`
  if (import.meta.client && navigator.share && project.value) {
    await navigator.share({ title: project.value.title, url })
    return
  }

  if (import.meta.client) {
    await navigator.clipboard?.writeText(url)
    showInfo({ title: 'اشتراک‌گذاری', message: 'لینک پروژه کپی شد.' })
  }
}

useHead(() => generateSeoMeta({
  title: project.value ? `${project.value.title} | آریا کرفت` : 'پروژه | آریا کرفت',
  description: project.value?.description?.slice(0, 160) || 'جزئیات پروژه در آریا کرفت',
  image: projectImage.value,
  url: `${requestUrl.origin}${route.fullPath}`,
  keywords: project.value?.skills?.map(skill => skill.name) ?? ['پروژه', 'آریا کرفت'],
  author: project.value?.user?.full_name || project.value?.user?.username || 'آریا کرفت',
  type: 'article',
}))
</script>
