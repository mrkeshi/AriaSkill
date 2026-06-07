import type { NotificationType } from '~/models/Notification/NotificationDTO'

// ─── Full style map (used in NotifBox & notifications pages) ───────────────
export interface NotifStyle {
  icon:        string
  iconBox:     string
  sideLine:    string
  borderHover: string
}

const NOTIF_STYLE_MAP: Record<string, NotifStyle> = {
  login_failed: {
    icon:        'mdi:shield-alert-outline',
    iconBox:     'border-rose-500/40 bg-rose-500/10 text-rose-400 shadow-[0_0_15px_rgba(244,63,94,0.15)]',
    sideLine:    'bg-rose-500',
    borderHover: 'hover:border-rose-500/30',
  },
  comment_created: {
    icon:        'mdi:comment-outline',
    iconBox:     'border-cyan-500/30 bg-cyan-500/10 text-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.1)]',
    sideLine:    'bg-cyan-500',
    borderHover: 'hover:border-cyan-500/30',
  },
  like_received: {
    icon:        'mdi:heart-outline',
    iconBox:     'border-amber-500/30 bg-amber-500/10 text-classic-gold shadow-[0_0_15px_rgba(212,175,55,0.1)]',
    sideLine:    'bg-classic-gold',
    borderHover: 'hover:border-classic-gold/30',
  },
  broadcast: {
    icon:        'mdi:bullhorn-outline',
    iconBox:     'border-purple-500/30 bg-purple-500/10 text-purple-400 shadow-[0_0_15px_rgba(168,85,247,0.1)]',
    sideLine:    'bg-purple-500',
    borderHover: 'hover:border-purple-500/30',
  },
}

const NOTIF_STYLE_FALLBACK: NotifStyle = {
  icon:        'mdi:bell-outline',
  iconBox:     'border-emerald-500/30 bg-emerald-500/10 text-emerald-400',
  sideLine:    'bg-emerald-500',
  borderHover: 'hover:border-emerald-500/30',
}

/** Returns the full style object for a notification type. */
export const notifStyle = (type: NotificationType | string): NotifStyle =>
  NOTIF_STYLE_MAP[type] ?? NOTIF_STYLE_FALLBACK

// ─── Icon-only helpers (used in NotificationDropdown header) ──────────────
const NOTIF_ICON_MAP: Record<string, string> = {
  login_failed:    'mdi:shield-alert-outline',
  comment_created: 'mdi:comment-text-outline',
  like_received:   'mdi:heart-outline',
  broadcast:       'mdi:bullhorn-outline',
}

const NOTIF_ICON_COLOR_MAP: Record<string, string> = {
  login_failed:    'text-rose-400 drop-shadow-[0_0_8px_rgba(244,63,94,0.5)]',
  comment_created: 'text-cyan-400 drop-shadow-[0_0_8px_rgba(6,182,212,0.5)]',
  like_received:   'text-classic-gold drop-shadow-[0_0_8px_rgba(212,175,55,0.5)]',
  broadcast:       'text-purple-400 drop-shadow-[0_0_8px_rgba(168,85,247,0.5)]',
}

/** Returns the MDI icon name for a notification type. */
export const notifIcon = (type: NotificationType | string): string =>
  NOTIF_ICON_MAP[type] ?? 'mdi:bell-badge-outline'

/** Returns the Tailwind color class for a notification type icon. */
export const notifIconColor = (type: NotificationType | string): string =>
  NOTIF_ICON_COLOR_MAP[type] ?? 'text-classic-gold drop-shadow-[0_0_8px_rgba(214,175,55,0.5)]'
