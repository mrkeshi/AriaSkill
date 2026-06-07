import type { ActivityType } from '~/models/Activity/ActivityDTO'

// ─── Full style (used in RecentActive — includes sidebar line) ─────────────
export interface ActivityStyleFull {
  icon:           string
  label:          string
  iconContainer:  string
  badge:          string
  line:           string
}

// ─── Compact style (used in activities page — no sidebar line) ────────────
export interface ActivityStyleCompact {
  icon:           string
  label:          string
  iconContainer:  string
  badge:          string
}

const ACTIVITY_MAP: Record<ActivityType, ActivityStyleFull> = {
  login_success: {
    icon:          'mdi:login',
    label:         'ورود موفق',
    iconContainer: 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400 shadow-[0_0_12px_rgba(16,185,129,0.1)]',
    badge:         'bg-emerald-500/10 text-emerald-400 border-emerald-500/10',
    line:          'bg-emerald-500',
  },
  login_failed: {
    icon:          'mdi:shield-alert-outline',
    label:         'ورود ناموفق',
    iconContainer: 'border-rose-500/30 bg-rose-500/10 text-rose-400 shadow-[0_0_12px_rgba(244,63,94,0.15)]',
    badge:         'bg-rose-500/10 text-rose-400 border-rose-500/10',
    line:          'bg-rose-500',
  },
  project_published: {
    icon:          'mdi:cloud-upload',
    label:         'انتشار پروژه',
    iconContainer: 'border-cyan-500/20 bg-cyan-500/10 text-cyan-400 shadow-[0_0_12px_rgba(6,182,212,0.1)]',
    badge:         'bg-cyan-500/10 text-cyan-400 border-cyan-500/10',
    line:          'bg-cyan-400',
  },
  project_created: {
    icon:          'mdi:folder-plus-outline',
    label:         'ایجاد پروژه',
    iconContainer: 'border-cyan-500/20 bg-cyan-500/10 text-cyan-400 shadow-[0_0_12px_rgba(6,182,212,0.1)]',
    badge:         'bg-cyan-500/10 text-cyan-400 border-cyan-500/10',
    line:          'bg-cyan-400',
  },
  project_updated: {
    icon:          'mdi:pencil-outline',
    label:         'ویرایش پروژه',
    iconContainer: 'border-blue-500/20 bg-blue-500/10 text-blue-400 shadow-[0_0_12px_rgba(59,130,246,0.1)]',
    badge:         'bg-blue-500/10 text-blue-400 border-blue-500/10',
    line:          'bg-blue-400',
  },
  project_deleted: {
    icon:          'mdi:folder-remove-outline',
    label:         'حذف پروژه',
    iconContainer: 'border-rose-500/20 bg-rose-500/10 text-rose-400 shadow-[0_0_12px_rgba(244,63,94,0.1)]',
    badge:         'bg-rose-500/10 text-rose-400 border-rose-500/10',
    line:          'bg-rose-500',
  },
  password_changed: {
    icon:          'mdi:lock-reset',
    label:         'تغییر رمز',
    iconContainer: 'border-amber-500/20 bg-amber-500/10 text-amber-400 shadow-[0_0_12px_rgba(245,158,11,0.1)]',
    badge:         'bg-amber-500/10 text-amber-400 border-amber-500/10',
    line:          'bg-amber-500',
  },
  project_documentation_downloaded: {
    icon:          'mdi:file-download-outline',
    label:         'دانلود مستندات',
    iconContainer: 'border-purple-500/20 bg-purple-500/10 text-purple-400 shadow-[0_0_12px_rgba(168,85,247,0.1)]',
    badge:         'bg-purple-500/10 text-purple-400 border-purple-500/10',
    line:          'bg-purple-500',
  },
  external_project_comment_created: {
    icon:          'mdi:comment-arrow-left-outline',
    label:         'دیدگاه در پروژه دیگران',
    iconContainer: 'border-indigo-500/20 bg-indigo-500/10 text-indigo-400 shadow-[0_0_12px_rgba(99,102,241,0.1)]',
    badge:         'bg-indigo-500/10 text-indigo-400 border-indigo-500/10',
    line:          'bg-indigo-400',
  },
  comment_created: {
    icon:          'mdi:comment-text-outline',
    label:         'ثبت دیدگاه',
    iconContainer: 'border-teal-500/20 bg-teal-500/10 text-teal-400 shadow-[0_0_12px_rgba(20,184,166,0.1)]',
    badge:         'bg-teal-500/10 text-teal-400 border-teal-500/10',
    line:          'bg-teal-400',
  },
}

const ACTIVITY_FALLBACK: ActivityStyleFull = {
  icon:          'mdi:information-outline',
  label:         'عمومی',
  iconContainer: 'border-white/10 bg-white/5 text-gray-400',
  badge:         'bg-white/10 text-gray-400 border-white/10',
  line:          'bg-gray-500',
}

/** Returns the full style object (icon, label, iconContainer, badge, line) for an activity type. */
export const activityStyle = (type: ActivityType | string): ActivityStyleFull =>
  ACTIVITY_MAP[type as ActivityType] ?? ACTIVITY_FALLBACK
