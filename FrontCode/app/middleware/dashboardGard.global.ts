import { useAuthStore } from "~/stores/authStore"; 

export default defineNuxtRouteMiddleware(async (to, from) => {
    if (to.path.toLocaleLowerCase().startsWith("/dashboard")) {
        const auth = useAuthStore();

        if (!auth.initialized) {
            await auth.initAuth();
        }

        if (!auth.isLogin) {
            return navigateTo("/user/login");
        }
    }
     if (to.path.toLocaleLowerCase().startsWith("/user")) {
        const auth = useAuthStore();

        if (auth.isLogin) {
            return navigateTo("/dashboard");
        }

    }
     if (to.path.toLocaleLowerCase().startsWith("/dashboard/admin")) {
        const auth = useAuthStore();

        if (!auth.isAdmin) {
            
            return navigateTo("/dashboard");
        }

    }
});
