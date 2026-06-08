// This file defines the types for the API response data transfer object (DTO) in a TypeScript project.
export interface ApiResponse<T> {
  success: boolean;
  code: number;
  data: T;
  errors: Record<string, any> | null;
  timestamp: string;
}
