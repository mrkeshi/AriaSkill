export interface StatCard {
  id:          number
  label:       string
  value:       number
  icon:        string
  iconStyle:   string
  shadowColor: string
  bgGlow:      string
  lineStyle:   string
}
export interface DashboardStatsDTO {
  total_projects: number
  total_downloads: number
  total_comments: number
  unread_notifications: number
}