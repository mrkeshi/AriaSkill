// Auth plugin to initialize authentication state on app startup
export default defineNuxtPlugin(async (nuxtApp) => {
const auth = useAuthStore();

    if (!auth.initialized) {
        await auth.initAuth();
    }
})
