export default defineNuxtPlugin(async (nuxtApp) => {
const auth = useAuthStore();
    

    if (!auth.initialized) {
        await auth.initAuth();
    }
})
