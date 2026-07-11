"use client";

import { motion } from "framer-motion";
import { Check, Play, FileText, Globe, Sparkles, Send, CheckCircle2 } from "lucide-react";

export type ApplicationStatus = "MATCH_PENDING" | "READY" | "PROCEEDED" | "CANCELLED" | "COMPLETED";

interface Props {
    status: ApplicationStatus | string;
    layout?: "horizontal" | "vertical";
}

interface Stage {
    id: number;
    label: string;
    description: string;
    icon: React.ReactNode;
}

const STAGES: Stage[] = [
    { id: 1, label: "Resume", description: "Uploaded & parsed", icon: <FileText className="w-3.5 h-3.5" /> },
    { id: 2, label: "Job", description: "Scraped requirements", icon: <Globe className="w-3.5 h-3.5" /> },
    { id: 3, label: "AI ", description: "Skill gap analysis", icon: <Sparkles className="w-3.5 h-3.5" /> },
    { id: 4, label: "Automation", description: "Started applying", icon: <Play className="w-3.5 h-3.5" /> },
    { id: 5, label: "Submitted", description: "Application sent", icon: <Send className="w-3.5 h-3.5" /> },
    { id: 6, label: "Completed", description: "Pipeline finished", icon: <CheckCircle2 className="w-3.5 h-3.5" /> },
];

export default function JourneyIndicator({ status, layout = "horizontal" }: Props) {
    // Determine active index based on backend status
    // MATCH_PENDING: stage 2 (Resume/Job done, match pending)
    // READY: stage 3 (Match done, ready to proceed)
    // CANCELLED: stopped at match stage
    // PROCEEDED: stage 4/5 (Automation started/submitted)
    // COMPLETED: stage 6 (Finished)
    const getActiveStageIndex = () => {
        switch (status) {
            case "MATCH_PENDING":
                return 2; // Up to Job Analysis completed, matching in progress
            case "READY":
                return 3; // Up to AI Match completed, waiting for proceed
            case "CANCELLED":
                return 3; // Match completed but cancelled
            case "PROCEEDED":
                return 5; // Automation & Submitted in progress
            case "COMPLETED":
                return 6; // All stages completed
            default:
                return 3;
        }
    };

    const activeIndex = getActiveStageIndex();

    if (layout === "horizontal") {
        return (
            <div className="w-full py-4 select-none">
                <div className="relative flex items-center justify-between">
                    {/* Connecting Background Line */}
                    <div className="absolute left-0 right-0 top-1/2 -translate-y-1/2 h-[2px] bg-slate-850 z-0" />
                    
                    {/* Connecting Active Progress Line */}
                    <div 
                        className="absolute left-0 top-1/2 -translate-y-1/2 h-[2px] bg-blue-500 transition-all duration-500 ease-out z-0"
                        style={{ width: `${((activeIndex - 1) / (STAGES.length - 1)) * 100}%` }}
                    />

                    {STAGES.map((stage, idx) => {
                        const isCompleted = idx + 1 < activeIndex || status === "COMPLETED";
                        const isActive = idx + 1 === activeIndex && status !== "COMPLETED" && status !== "CANCELLED";
                        const isCancelled = status === "CANCELLED" && idx + 1 === 3;
                        const isPending = !isCompleted && !isActive && !isCancelled;

                        return (
                            <div key={stage.id} className="flex flex-col items-center z-10 relative">
                                {/* Dot Indicator */}
                                <div
                                    className={`flex h-6 w-6 items-center justify-center rounded-full border-2 transition-all duration-300 ${
                                        isCompleted
                                            ? "bg-emerald-500/10 border-emerald-500 text-emerald-400"
                                            : isCancelled
                                            ? "bg-red-500/10 border-red-500 text-red-400"
                                            : isActive
                                            ? "bg-blue-600/10 border-blue-500 text-blue-400 pulse-glow-blue"
                                            : "bg-slate-950 border-slate-800 text-slate-500"
                                    }`}
                                >
                                    {isCompleted ? (
                                        <Check className="w-3 h-3 stroke-[3px]" />
                                    ) : (
                                        stage.icon
                                    )}
                                </div>

                                {/* Mini Label */}
                                <span
                                    className={`text-[9px] font-bold mt-2 tracking-tight transition-colors duration-300 ${
                                        isCompleted
                                            ? "text-slate-400"
                                            : isCancelled
                                            ? "text-red-400"
                                            : isActive
                                            ? "text-blue-400 font-extrabold"
                                            : "text-slate-600"
                                    }`}
                                >
                                    {stage.label}
                                </span>
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }

    // Vertical detailed journey (for drawers and mobile views)
    return (
        <div className="flex flex-col gap-6 py-2">
            {STAGES.map((stage, idx) => {
                const isCompleted = idx + 1 < activeIndex || status === "COMPLETED";
                const isActive = idx + 1 === activeIndex && status !== "COMPLETED" && status !== "CANCELLED";
                const isCancelled = status === "CANCELLED" && idx + 1 === 3;
                const isPending = !isCompleted && !isActive && !isCancelled;

                return (
                    <div key={stage.id} className="flex gap-4 relative">
                        {/* Connecting vertical line */}
                        {idx < STAGES.length - 1 && (
                            <div className="absolute left-[0.875rem] top-7 bottom-[-1.5rem] w-[1.5px] bg-slate-850 z-0">
                                <div
                                    className="w-full bg-blue-500 transition-all duration-500"
                                    style={{ height: isCompleted ? "100%" : "0%" }}
                                />
                            </div>
                        )}

                        {/* Ring Icon */}
                        <div className="z-10 relative">
                            <div
                                className={`flex h-7 w-7 items-center justify-center rounded-full border-2 transition-all duration-300 ${
                                    isCompleted
                                        ? "bg-emerald-500/10 border-emerald-500 text-emerald-400 shadow-lg shadow-emerald-950/20"
                                        : isCancelled
                                        ? "bg-red-500/10 border-red-500 text-red-400"
                                        : isActive
                                        ? "bg-blue-600/10 border-blue-500 text-blue-400 pulse-glow-blue"
                                        : "bg-slate-900 border-slate-800 text-slate-500"
                                }`}
                            >
                                {isCompleted ? (
                                    <Check className="w-3.5 h-3.5 stroke-[3px]" />
                                ) : (
                                    stage.icon
                                )}
                            </div>
                        </div>

                        {/* Labels & Description */}
                        <div className="flex flex-col select-text">
                            <span
                                className={`text-xs font-bold transition-colors duration-300 ${
                                    isCompleted
                                        ? "text-slate-200"
                                        : isCancelled
                                        ? "text-red-400"
                                        : isActive
                                        ? "text-blue-400 font-extrabold"
                                        : "text-slate-500"
                                }`}
                            >
                                {stage.label}
                            </span>
                            <span
                                className={`text-[10px] mt-0.5 transition-colors duration-300 ${
                                    isCompleted
                                        ? "text-slate-500"
                                        : isActive
                                        ? "text-slate-400"
                                        : "text-slate-600"
                                }`}
                            >
                                {isCancelled ? "Application cancelled by user" : stage.description}
                            </span>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
