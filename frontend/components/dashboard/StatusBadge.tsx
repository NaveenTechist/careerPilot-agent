"use client";

import { motion } from "framer-motion";

type Props = {
    status: string;
};

const STATUS_MAP: Record<string, { label: string; classes: string; pulse?: boolean }> = {
    READY: {
        label: "Pending",
        classes: "bg-blue-500/10 text-blue-400 border-blue-500/20",
        pulse: true,
    },
    MATCH_PENDING: {
        label: "Pending",
        classes: "bg-blue-500/10 text-blue-400 border-blue-500/20",
        pulse: true,
    },
    PENDING: {
        label: "Pending",
        classes: "bg-blue-500/10 text-blue-400 border-blue-500/20",
        pulse: true,
    },
    CANCELLED: {
        label: "Cancelled",
        classes: "bg-red-500/10 text-red-400 border-red-500/20",
    },
    PROCEEDED: {
        label: "Proceeded",
        classes: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    },
    COMPLETED: {
        label: "Completed",
        classes: "bg-purple-500/10 text-purple-400 border-purple-500/20",
    },
};

export default function StatusBadge({ status }: Props) {
    const config = STATUS_MAP[status] || STATUS_MAP.PENDING;
    return (
        <motion.span
            initial={{ scale: 0.85, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: "spring", stiffness: 350, damping: 22 }}
            className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-[11px] font-bold uppercase tracking-wider select-none ${config.classes}`}
        >
            {config.pulse && (
                <span className="relative flex h-1.5 w-1.5">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75" />
                    <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-blue-400" />
                </span>
            )}
            {config.label}
        </motion.span>
    );
}
