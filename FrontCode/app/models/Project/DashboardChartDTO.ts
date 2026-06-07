export interface DashboardChartDTO {
  /** ISO date strings, e.g. ["2026-05-20", "2026-05-21", ...] (max 20 items) */
  days: string[]
  /** Daily activity/view counts aligned with days[] */
  views: number[]
  /** Daily download counts aligned with days[] */
  downloads: number[]
}
