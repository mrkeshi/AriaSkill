import { defineStore } from "pinia";
import type { AuthUserDTO, LoginDTO } from "~/models/User/AuthDTO";
import type { UserDTO } from "~/models/User/UserDTO";
import { fetchUserService, googleAuthService, LoginUserService, refreshTokenService } from "~/services/user/user.Service";
import { createEmptyUser, normalizeAuthUser, type AuthUserResponse } from "~/utilities/authUser";

export const useAuthStore = defineStore("AuthStore", () => {
  const router = useRouter();

  const isLogin = ref(false);
  const initialized = ref(false);
  const user = reactive<UserDTO>(createEmptyUser());

  const accessTokenCookie = useCookie<string | null>('accessToken', { maxAge: 60 * 60 * 24 });
  const refreshTokenCookie = useCookie<string | null>('refreshToken', { maxAge: 60 * 60 * 24 * 7 });

  const isAdmin = computed(() => user.is_staff || user.is_superuser);

  const applyAuth = async (data: AuthUserDTO) => {
    accessTokenCookie.value = data.access;
    refreshTokenCookie.value = data.refresh;
    Object.assign(user, normalizeAuthUser(data.user as AuthUserResponse));
    isLogin.value = true;
    await fetchUser();
    initialized.value = true;
    router.push({ name: 'dashboard' });
  };

  const login = async (input: LoginDTO) => {
    const res = await LoginUserService(input);
    await applyAuth(res.data);
  };

  const loginWithGoogle = async (credential: string) => {
    const res = await googleAuthService(credential);
    await applyAuth(res.data);
  };

  /**
   * FIX: "Maximum call stack size exceeded"
   *
   * The original bug was a circular call loop:
   *   initAuth() → fetchUser() → [on error] logout() → sets initialized = false
   *   → middleware sees !initialized → calls initAuth() again → infinite recursion.
   *
   * The fix: logout() no longer resets `initialized` to false.
   * The `initialized` flag marks that the bootstrap attempt has completed,
   * regardless of the outcome. Resetting it caused the middleware and plugin
   * to re-trigger initAuth() on every navigation, creating the stack overflow.
   */
  const logout = async () => {
    accessTokenCookie.value = null;
    refreshTokenCookie.value = null;
    isLogin.value = false;
    // ✅ Do NOT reset initialized here — that was the source of the infinite loop.
    // initialized stays true so the middleware knows auth was already attempted.
    router.push({ name: 'user-login' });
  };

  const fetchUser = async () => {
    try {
      const res = await fetchUserService();
      Object.assign(user, normalizeAuthUser(res.data as AuthUserResponse));
      isLogin.value = true;
    } catch (e) {
 
      accessTokenCookie.value = null;
      refreshTokenCookie.value = null;
      isLogin.value = false;
    }
  };

  const tryRefreshToken = async (): Promise<boolean> => {
    if (!refreshTokenCookie.value) return false;

    try {
      const res = await refreshTokenService(refreshTokenCookie.value);
      accessTokenCookie.value = res.data.access;
      if (res.data.refresh) {
        refreshTokenCookie.value = res.data.refresh;
      }
      return true;
    } catch (e) {
      return false;
    }
  };

  const initAuth = async () => {
    if (initialized.value) return;

    if (!accessTokenCookie.value) {
      const success = await tryRefreshToken();
      if (!success) {
        initialized.value = true;
        return;
      }
      isLogin.value = true;
    }

    await fetchUser();
    initialized.value = true;
  };

  return { isLogin, user, isAdmin, logout, login, loginWithGoogle, fetchUser, initialized, initAuth, tryRefreshToken, accessTokenCookie };
});
