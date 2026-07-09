"use client";

import { motion } from "framer-motion";
import { FileSearch, Plus, Sparkles } from "lucide-react";

type Props = {
    onNewApplication: () => void;
};

export default function EmptyState({ onNewApplication }: Props) {
    return (
        <div className="flex flex-col items-center justify-center py-20 px-6 text-center">
            {/* Illustration with floating animation */}
            <motion.div
                className="relative mb-8"
                animate={{ y: [0, -8, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            >
                <div className="flex h-24 w-24 items-center justify-center rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl shadow-slate-950/50">
                    <FileSearch className="w-10 h-10 text-slate-600" />
                </div>
                <motion.div
                    className="absolute -bottom-1 -right-1 flex h-8 w-8 items-center justify-center rounded-xl bg-blue-600 text-white shadow-lg shadow-blue-950/50"
                    animate={{ scale: [1, 1.15, 1] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
                >
                    <Plus className="w-4 h-4 stroke-[3px]" />
                </motion.div>
            </motion.div>

            <motion.h3
                className="text-xl font-bold text-slate-200 tracking-tight"
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.15 }}
            >
                No Applications Yet
            </motion.h3>
            <motion.p
                className="mt-2 text-sm text-slate-500 max-w-xs leading-relaxed"
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.25 }}
            >
                Create your first application to start matching your resume with job postings using AI.
            </motion.p>

            <motion.button
                onClick={onNewApplication}
                className="mt-8 inline-flex items-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-500 px-7 py-3 text-sm font-bold text-white shadow-lg shadow-blue-950/40 transition-all duration-200 active:translate-y-0.5 cursor-pointer"
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.35 }}
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
            >
                <Sparkles className="w-4 h-4" />
                Create First Application
            </motion.button>
        </div>
    );
}
