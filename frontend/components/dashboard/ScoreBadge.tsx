"use client";

import { motion } from "framer-motion";

type Props = {
    score: number;
};

export default function ScoreBadge({ score }: Props) {
    const getColors = () => {
        if (score >= 90) return "text-emerald-400 bg-emerald-500/10 border-emerald-500/20";
        if (score >= 75) return "text-blue-400 bg-blue-500/10 border-blue-500/20";
        if (score >= 60) return "text-amber-400 bg-amber-500/10 border-amber-500/20";
        return "text-red-400 bg-red-500/10 border-red-500/20";
    };

    return (
        <motion.span
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: "spring", stiffness: 400, damping: 20 }}
            className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-extrabold tabular-nums select-none ${getColors()}`}
        >
            {score}%
        </motion.span>
    );
}
