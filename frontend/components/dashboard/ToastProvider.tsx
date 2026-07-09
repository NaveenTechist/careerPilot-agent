"use client";

import React, { createContext, useContext, useState, useCallback } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { CheckCircle2, XCircle, AlertTriangle, Info, X } from "lucide-react";

export type ToastType = "success" | "error" | "warning" | "info";

export interface ToastItem {
    id: string;
    message: string;
    type: ToastType;
    duration?: number;
}

interface ToastContextType {
    toasts: ToastItem[];
    addToast: (message: string, type?: ToastType, duration?: number) => void;
    removeToast: (id: string) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export function useToastContext() {
    const context = useContext(ToastContext);
    if (!context) {
        throw new Error("useToastContext must be used within a ToastProvider");
    }
    return context;
}

export default function ToastProvider({ children }: { children: React.ReactNode }) {
    const [toasts, setToasts] = useState<ToastItem[]>([]);

    const addToast = useCallback((message: string, type: ToastType = "info", duration = 4000) => {
        const id = Math.random().toString(36).substring(2, 9);
        setToasts((prev) => [...prev, { id, message, type, duration }]);
    }, []);

    const removeToast = useCallback((id: string) => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
    }, []);

    return (
        <ToastContext.Provider value={{ toasts, addToast, removeToast }}>
            {children}
            {/* Toast Container Stack */}
            <div className="fixed top-6 right-4 sm:right-6 z-[100] flex flex-col gap-3 w-full max-w-sm pointer-events-none">
                <AnimatePresence mode="popLayout">
                    {toasts.map((toast) => (
                        <Toast key={toast.id} toast={toast} onDismiss={removeToast} />
                    ))}
                </AnimatePresence>
            </div>
        </ToastContext.Provider>
    );
}

function Toast({ toast, onDismiss }: { toast: ToastItem; onDismiss: (id: string) => void }) {
    const { id, message, type, duration = 4000 } = toast;

    React.useEffect(() => {
        const timer = setTimeout(() => {
            onDismiss(id);
        }, duration);
        return () => clearTimeout(timer);
    }, [id, duration, onDismiss]);

    const getStyles = () => {
        switch (type) {
            case "success":
                return {
                    icon: <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />,
                    border: "border-emerald-500/25",
                    glow: "shadow-emerald-950/20",
                    progress: "bg-emerald-500",
                };
            case "error":
                return {
                    icon: <XCircle className="w-5 h-5 text-red-400 shrink-0" />,
                    border: "border-red-500/25",
                    glow: "shadow-red-950/20",
                    progress: "bg-red-500",
                };
            case "warning":
                return {
                    icon: <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />,
                    border: "border-amber-500/25",
                    glow: "shadow-amber-950/20",
                    progress: "bg-amber-500",
                };
            case "info":
            default:
                return {
                    icon: <Info className="w-5 h-5 text-blue-400 shrink-0" />,
                    border: "border-blue-500/25",
                    glow: "shadow-blue-950/20",
                    progress: "bg-blue-500",
                };
        }
    };

    const styles = getStyles();

    return (
        <motion.div
            layout
            initial={{ opacity: 0, y: -20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.85, transition: { duration: 0.15 } }}
            className={`glass-toast rounded-2xl p-4 shadow-2xl border ${styles.border} ${styles.glow} flex flex-col gap-2 pointer-events-auto overflow-hidden relative w-full`}
        >
            <div className="flex items-start gap-3">
                {/* Icon */}
                <div className="mt-0.5">{styles.icon}</div>

                {/* Content */}
                <div className="flex-1 min-w-0 pr-2">
                    <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest leading-none">
                        {type}
                    </p>
                    <p className="text-sm font-medium text-slate-200 mt-1.5 leading-relaxed">
                        {message}
                    </p>
                </div>

                {/* Close Button */}
                <button
                    onClick={() => onDismiss(id)}
                    className="rounded-lg p-1 text-slate-500 hover:bg-slate-900/60 hover:text-slate-350 transition-colors shrink-0 cursor-pointer"
                    aria-label="Close notification"
                >
                    <X className="h-4 w-4" />
                </button>
            </div>

            {/* Visual Progress Bar Timer */}
            <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-slate-900/30">
                <motion.div
                    initial={{ width: "100%" }}
                    animate={{ width: "0%" }}
                    transition={{ duration: duration / 1000, ease: "linear" }}
                    className={`h-full ${styles.progress}`}
                />
            </div>
        </motion.div>
    );
}
