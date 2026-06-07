import { FetchError } from "ofetch";
import type { NitroFetchOptions } from "nitropack";
import type { ApiResponse } from "~/models/ApiResponseDTO";
import { baseURL as BASE_URL } from "./ApiConfig";
import { useCustomToastify } from "~/composable/useCustomToasitify";
import { useAuthStore } from "~/stores/authStore";


const { showError } = useCustomToastify();

export async function FetchX<T>(
  url: string,
  config: NitroFetchOptions<string> = {}
): Promise<ApiResponse<T>> {
const nuxtconfug = useRuntimeConfig()
  const authStore = useAuthStore();
  const accessTokenCookie = useCookie<string | null>('accessToken');
  config = {
    baseURL: nuxtconfug.public.baseUrl as string,
    ...config,
    headers: {
      ...(config.headers || {})
    }
  };

  if (accessTokenCookie.value) {
    (config.headers as Record<string, string>)["Authorization"] = `JWT ${accessTokenCookie.value}`;
  }

  try {
    return await $fetch<ApiResponse<T>>(url, config);
  } catch (e: any) {
    
    if (e.response?.status === 401) {
      const isRefreshed = await authStore.tryRefreshToken();
      
      if (isRefreshed) {
        (config.headers as Record<string, string>)["Authorization"] = `JWT ${accessTokenCookie.value}`;
        return await $fetch<ApiResponse<T>>(url, config);
      } else {
        authStore.logout();
      }
    }


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
