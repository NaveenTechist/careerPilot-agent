"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, XCircle, AlertTriangle, Info, X } from "lucide-react";

type Props = {
    open: boolean;
    message: string;
    onClose?: () => void;
};

export default function Notification({
    open,
    message,
    onClose,
}: Props) {
    const [shouldRender, setShouldRender] = useState(open);

    useEffect(() => {
        if (open) {
            setShouldRender(true);
        } else {
            // Animate close before unmounting or hiding
            const timer = setTimeout(() => setShouldRender(false), 200);
            return () => clearTimeout(timer);
        }
    }, [open]);

    if (!shouldRender) return null;

    // Detect type based on message text
    const getNotificationType = () => {
        const text = message.toLowerCase();
        if (text.includes("success") || text.includes("completed") || text.includes("started") || text.includes("uploaded")) {
            return "success";
        }
        if (text.includes("fail") || text.includes("error") || text.includes("unable") || text.includes("invalid")) {
            return "error";
        }
        if (text.includes("cancel") || text.includes("warning") || text.includes("already")) {
            return "warning";
        }
        return "info";
    };

    const type = getNotificationType();

    const getStyles = () => {
        switch (type) {
            case "success":
                return {
                    icon: <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />,
                    border: "border-emerald-500/25",
                    glow: "shadow-emerald-950/20"
                };
            case "error":
                return {
                    icon: <XCircle className="w-5 h-5 text-red-400 shrink-0" />,
                    border: "border-red-500/25",
                    glow: "shadow-red-950/20"
                };
            case "warning":
                return {
                    icon: <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />,
                    border: "border-amber-500/25",
                    glow: "shadow-amber-950/20"
                };
            case "info":
            default:
                return {
                    icon: <Info className="w-5 h-5 text-blue-400 shrink-0" />,
                    border: "border-blue-500/25",
                    glow: "shadow-blue-950/20"
                };
        }
    };

    const styles = getStyles();

    return (
        <div
            className={`fixed right-4 sm:right-6 top-6 z-[60] max-w-sm w-full sm:w-[360px] glass-toast rounded-2xl px-4 py-3.5 shadow-2xl border ${
                styles.border
            } ${styles.glow} flex items-start gap-3.5 transition-all duration-200 ${
                open ? "animate-slide-in" : "opacity-0 translate-y-[-10px] scale-95"
            }`}
        >
            {/* Type Icon */}
            <div className="mt-0.5">{styles.icon}</div>

            {/* Content info */}
            <div className="flex-1 min-w-0 pr-2">
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest leading-none">
                    Notification
                </p>
                <p className="text-sm font-medium text-slate-200 mt-1.5 leading-relaxed">
                    {message}
                </p>
            </div>

            {/* Close Button */}
            {onClose && (
                <button
                    onClick={onClose}
                    className="rounded-lg p-1 text-slate-500 hover:bg-slate-900 hover:text-slate-300 transition-colors shrink-0 mt-0.5"
                    aria-label="Close notification"
                >
                    <X className="h-4 w-4" />
                </button>
            )}
        </div>
    );
}