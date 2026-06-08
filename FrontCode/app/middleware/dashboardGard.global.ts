import { useAuthStore } from "~/stores/authStore"; 
// This middleware checks if the user is authenticated before allowing access to the dashboard routes. 
// If the user is not authenticated, they will be redirected to the login page. Additionally, 
// it checks if the user is an admin before allowing access to admin routes within the dashboard.
// If the user is not an admin, they will be redirected back to the main dashboard page.
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
