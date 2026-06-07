<template>
  <form dir="rtl" class="grid grid-cols-1 lg:grid-cols-3 gap-6" @submit.prevent="submit">

    <div class="lg:col-span-2 space-y-5">


      <UiInput
        name="title"
        label="عنوان پروژه"
        placeholder="مثلاً: سامانه مدیریت فروشگاه"
        :model-value="form.title"
        :ignore-error-message="true"
        rtl
        @update:model-value="form.title = $event"
      />

      <div class="space-y-2">
  <label class="block text-sm font-medium mb-2 text-bone-white">نوع پروژه</label>

  <div class="relative">
    <select
      v-model="form.project_type"
      required
      class="w-full px-4 py-3 pl-10 rounded-lg border border-gray-300 focus:ring-1 focus:ring-classic-gold focus:border-classic-gold outline-none transition-all bg-transparent text-white [&>option]:bg-slate-900 appearance-none"
    >
      <option value="" disabled>نوع پروژه را انتخاب کنید</option>
      <option v-for="type in PROJECT_TYPES" :key="type.value" :value="type.value">
        {{ type.label }}
      </option>
    </select>

    <svg
      class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
    </svg>
  </div>
</div>



      <UiTextarea
        name="description"
        label="توضیحات پروژه"
        placeholder="توضیحات واضحی درباره هدف، امکانات و تکنولوژی‌های پروژه بنویسید."
        :rows="7"
        :model-value="form.description"
        :ignore-error-message="true"
        rtl
        @update:model-value="form.description = $event"
      />

      <DashboardProjectFormSkillSearch
        :selected-skills="selectedSkills"
        @toggle="toggleSkill"
      />
    </div>

    <div class="space-y-5">

      <DashboardProjectFormCoverImagePicker
        :initial-url="initialImageUrl"
        @change="form.image = $event"
      />

      <UiFileAttachment
        name="project_file"
        label="فایل پروژه"
        accept=".zip,.rar,.tar.gz,.pdf"
        placeholder="انتخاب فایل ZIP، RAR، TAR.GZ یا PDF"
        hint="حداکثر حجم: ۵۰ مگابایت"
        :model-value="form.file ?? undefined"
        @update:model-value="form.file = $event"
      />

      <div class="flex flex-col gap-3 pt-2">
        <UiButton type="submit" variant="gold" full :disabled="loading">
          {{ loading ? 'در حال ذخیره...' : submitLabel }}
        </UiButton>
        <UiButton type="button" variant="outline" full :disabled="loading" @click="$emit('cancel')">
          انصراف
        </UiButton>
      </div>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import type { ProjectDTO } from '~/models/Project/ProjectDTO'
import type { skillItem } from '~/models/Skill/SkillDTO'
import { resolveMediaUrl } from '~/utilities/urlHelpers'

const props = withDefaults(defineProps<{
  initialProject?: ProjectDTO | null
  loading?: boolean
  submitLabel?: string
}>(), {
  initialProject: null,
  loading: false,
  submitLabel: 'ذخیره پروژه',
})

const emit = defineEmits<{
  submit: [formData: FormData]
  cancel: []
}>()

// ─── consts ────────────────────────────────────────────────────
const PROJECT_TYPES = [
  { value: 'UI/UX',        label: 'طراحی UI/UX' },
  { value: 'Frontend',     label: 'توسعه فرانت‌اند' },
  { value: 'Backend',      label: 'توسعه بک‌اند' },
  { value: 'Mobile',       label: 'توسعه موبایل' },
  { value: 'AI_Data',      label: 'هوش مصنوعی و داده' },
  { value: 'DevOps_Cloud', label: 'DevOps و فضای ابری' },
  { value: 'Game',         label: 'توسعه بازی' },
  { value: 'Cyber_Sec',    label: 'امنیت سایبری' },
]

// ─── state ──────────────────────────────────────────────────────
const form = reactive({
  title: '',
  project_type: '',
  description: '',
  image: null as File | null,
  file: null as File | null,
})

const selectedSkills = ref<skillItem[]>([])
const initialImageUrl = ref('')

// ─── helpers ────────────────────────────────────────────────────
const toggleSkill = (skill: skillItem) => {
  const exists = selectedSkills.value.some(s => s.id === skill.id)
  selectedSkills.value = exists
    ? selectedSkills.value.filter(s => s.id !== skill.id)
    : [...selectedSkills.value, skill]
}

const buildFormData = (): FormData => {
  const fd = new FormData()
  fd.append('title', form.title)
  fd.append('project_type', form.project_type)
  fd.append('description', form.description)
  selectedSkills.value.forEach(s => fd.append('skill_ids', String(s.id)))
  if (form.image) fd.append('image', form.image)
  if (form.file)  fd.append('file', form.file)
  return fd
}

const hydrate = (project?: ProjectDTO | null) => {
  form.title        = project?.title        ?? ''
  form.project_type = project?.project_type ?? ''
  form.description  = project?.description  ?? ''
  form.image        = null
  form.file         = null
  selectedSkills.value  = project?.skills ? [...project.skills] : []
  initialImageUrl.value = resolveMediaUrl(project?.image)
}

const submit = () => emit('submit', buildFormData())

// ─── watchers ───────────────────────────────────────────────────
watch(() => props.initialProject, hydrate, { immediate: true })



</script>


