import { defineStore } from "pinia";
import type { AuthUserDTO, LoginDTO } from "~/models/User/AuthDTO";
import type { UserDTO } from "~/models/User/UserDTO";
import { fetchUserService, googleAuthService, LoginUserService, refreshTokenService } from "~/services/user/user.Service";
import { createEmptyUser, normalizeAuthUser, type AuthUserResponse } from "~/utilities/authUser";

/**
 * Pinia store for handling user authentication, session state, 
 * token persistence (via Nuxt cookies), and role-based permissions.
 */
export const useAuthStore = defineStore("AuthStore", () => {
  const router = useRouter();

  // --- Reactive States ---
  const isLogin = ref(false);        // Tracks if the user is currently authenticated
  const initialized = ref(false);    // Ensures the authentication check runs only once during app startup
  const user = reactive<UserDTO>(createEmptyUser()); // Stores current user profile details

  // --- Token Cookie Storage ---
  // Access Token: Valid for 24 hours
  const accessTokenCookie = useCookie<string | null>('accessToken', { maxAge: 60 * 60 * 24 });
  // Refresh Token: Valid for 7 days
  const refreshTokenCookie = useCookie<string | null>('refreshToken', { maxAge: 60 * 60 * 24 * 7 });

  // --- Getters / Computed Properties ---
  // Computes whether the authenticated user has administrative privileges
  const isAdmin = computed(() => user.is_staff || user.is_superuser);

  // --- Helper Actions ---
  /**
   * Commits the tokens and user profile to cookies and state,
   * refetches full profile, and redirects to the dashboard.
   * @param {AuthUserDTO} data - The payload containing tokens and user metadata.
   */
  const applyAuth = async (data: AuthUserDTO) => {
    accessTokenCookie.value = data.access;
    refreshTokenCookie.value = data.refresh;
    Object.assign(user, normalizeAuthUser(data.user as AuthUserResponse));
    isLogin.value = true;
    
    await fetchUser();
    initialized.value = true;
    router.push({ name: 'dashboard' });
  };

  // --- Authentication Actions ---
  /**
   * Standard Username/Password login workflow.
   * @param {LoginDTO} input - Form credentials.
   */
  const login = async (input: LoginDTO) => {
    const res = await LoginUserService(input);
    await applyAuth(res.data);
  };

  /**
   * Authenticates user using Google Identity Services credential token.
   * @param {string} credential - The JWT token provided by Google OAuth.
   */
  const loginWithGoogle = async (credential: string) => {
    const res = await googleAuthService(credential);
    await applyAuth(res.data);
  };

  /**
   * Clears authentication session, revokes local cookies, and routes back to login view.
   */
  const logout = async () => {
    accessTokenCookie.value = null;
    refreshTokenCookie.value = null;
    isLogin.value = false;

    router.push({ name: 'user-login' });
  };

  /**
   * Requests the current authenticated user's profile data from the server.
   * Flushes tokens if the backend authorization fails (e.g., token expired/invalidated).
   */
  const fetchUser = async () => {
    try {
      const res = await fetchUserService();
      Object.assign(user, normalizeAuthUser(res.data as AuthUserResponse));
      isLogin.value = true;
    } catch (e) {
      // Invalidate auth state on user data fetch failures
      accessTokenCookie.value = null;
      refreshTokenCookie.value = null;
      isLogin.value = false;
    }
  };

  /**
   * Attempts to request a new access token using the active refresh token.
   * @returns {Promise<boolean>} Resolves to true if token rotation succeeded, false otherwise.
   */
  const tryRefreshToken = async (): Promise<boolean> => {
    if (!refreshTokenCookie.value) return false;

    try {
      const res = await refreshTokenService(refreshTokenCookie.value);
      accessTokenCookie.value = res.data.access;
      if (res.data.refresh) {
        refreshTokenCookie.value = res.data.refresh; // Update refresh token if rotated by backend
      }
      return true;
    } catch (e) {
      return false;
    }
  };

  /**
   * Bootstraps authentication state on application startup.
   * Implements silent refresh if access token is missing but refresh token exists.
   */
  const initAuth = async () => {
    if (initialized.value) return;

    if (!accessTokenCookie.value) {
      const success = await tryRefreshToken();
      if (!success) {
        initialized.value = true;
        return; // Halt lifecycle if both tokens are missing/expired
      }
      isLogin.value = true;
    }

    await fetchUser();
    initialized.value = true;
  };

  return { isLogin, user, isAdmin, logout, login, loginWithGoogle, fetchUser, initialized, initAuth, tryRefreshToken, accessTokenCookie };
});