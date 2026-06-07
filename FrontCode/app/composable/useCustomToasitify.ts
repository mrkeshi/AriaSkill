    import type { ToastParams } from "~/models/ToastifyDTO"

    export function useCustomToastify() {
    const showError = ({
        title,
        message,
        type = 'error',
        theme = 'dark',
        autoClose = 3000,  
        toastId,
        icon,
        rtl = true,
        hideProgressBar = false,
    }: ToastParams) => {
        useToastify(`${title}<br>${message}`, {
        type,
        theme,
        toastId,
        autoClose,
        dangerouslyHTMLString: true,
        icon,
        rtl,
        hideProgressBar,
        toastClassName: 'custom-toast',
        bodyClassName: 'custom-toast-body',
        })
    }
    const showInfo = ({
    title,
    message,
    toastId,
    icon,
    rtl = true,
    autoClose = 3000,
    }: ToastParams) => {
    useToastify(`${title}<br>${message}`, {
        type: 'info',
        theme: 'dark',
        autoClose,
        toastId,
        icon,
        rtl,
        hideProgressBar: false,
        dangerouslyHTMLString: true,
        toastClassName: 'custom-toast',
        bodyClassName: 'custom-toast-body',
    })
    }

    const showSuccess = ({
        title,
        message,
        toastId,
        icon,
        rtl = true,
        autoClose = 3000,  
    }: ToastParams) => {
        useToastify(`${title}<br>${message}`, {
        type: 'success',
        theme: 'dark',
        autoClose,
        toastId,
        icon,
        rtl,
        hideProgressBar: false,
        dangerouslyHTMLString: true,
        toastClassName: 'custom-toast',
        bodyClassName: 'custom-toast-body',
        })
    }

    return { showError, showSuccess,showInfo }
    }
