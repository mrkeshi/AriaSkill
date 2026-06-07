export interface ApiResponse<T> {
  success: boolean;
  code: number;
  data: T;
  errors: Record<string, any> | null;
  timestamp: string;
}
