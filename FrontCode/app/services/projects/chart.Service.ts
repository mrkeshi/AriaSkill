// This file defines the services for handling chart-related operations in a TypeScript project.
import type { ApiResponse } from '~/models/ApiResponseDTO'
import type { DashboardChartDTO } from '~/models/Project/DashboardChartDTO'
import { FetchX } from '~/utilities/fetchX'

export const getDashboardChartService = (): Promise<ApiResponse<DashboardChartDTO>> => {
  return FetchX('project/dashboard/chart/', { method: 'get' })
}
