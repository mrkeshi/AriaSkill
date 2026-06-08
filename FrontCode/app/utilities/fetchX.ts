import type { NitroFetchOptions } from "nitropack";
import type { ApiResponse } from "~/models/ApiResponseDTO";
import { useCustomToastify } from "~/composable/useCustomToasitify";
import { useAuthStore } from "~/stores/authStore";

const { showError } = useCustomToastify();

/**
 * High-performance global HTTP client engine wrapped around Nuxt $fetch.
 * Automatically handles JWT Authorization states, reactive token refreshing on 401 statuses,
 * and normalizes disparate multi-type validation error packets into safe user toast notifications.
 */
export async function FetchX<T>(
  url: string,
  config: NitroFetchOptions<string> = {}
): Promise<ApiResponse<T>> {
  const nuxtConfig = useRuntimeConfig()
  const authStore = useAuthStore();
  const accessTokenCookie = useCookie<string | null>('accessToken');

  // ── Configure Base Fetch Target Environment ──────────────────────────────
  config = {
    baseURL: nuxtConfig.public.baseUrl as string,
    ...config,
    headers: {
      ...(config.headers || {})
    }
  };

  // ── Inject Authentication Headers If Present ─────────────────────────────
  if (accessTokenCookie.value) {
    (config.headers as Record<string, string>)["Authorization"] = `JWT ${accessTokenCookie.value}`;
  }

  try {
    return await $fetch<ApiResponse<T>>(url, config);
  } catch (e: any) {
    
    // ── Handle Token Expiration Interception (401 Unauthorized) ──────────────
    if (e.response?.status === 401) {
      const isRefreshed = await authStore.tryRefreshToken();
      
      if (isRefreshed) {
        (config.headers as Record<string, string>)["Authorization"] = `JWT ${accessTokenCookie.value}`;
        return await $fetch<ApiResponse<T>>(url, config);
      } else {
        authStore.logout();
      }
    }

    // ── Dynamic Server Error Normalization & Message Parsing ─────────────────
    const errors = e?.data?.errors;

    if (!errors) {
      showError({
        title: "خطا",
        message: e?.message || "خطای نامشخص",
      });
    } else if (typeof errors === "string") {
      showError({
        title: "خطا",
        message: errors,
      });
    } else if (typeof errors === "object") {
      Object.entries(errors).forEach(([key, value]) => {
        showError({
          title: "خطا",
          message: `${key}: ${value}`,
        });
      });
    }

    throw e;
  }
}