"use client";

import { useToastContext } from "@/components/dashboard/ToastProvider";

export function useAppToast() {
    const { addToast } = useToastContext();

    const toastSuccess = (message: string, duration?: number) => {
        addToast(message, "success", duration);
    };

    const toastError = (message: string, duration?: number) => {
        addToast(message, "error", duration);
    };

    const toastWarning = (message: string, duration?: number) => {
        addToast(message, "warning", duration);
    };

    const toastInfo = (message: string, duration?: number) => {
        addToast(message, "info", duration);
    };

    return {
        toastSuccess,
        toastError,
        toastWarning,
        toastInfo,
        addToast,
    };
}
