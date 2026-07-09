"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Check, Loader2, Play, AlertCircle } from "lucide-react";

export type ProcessingStatus = "processing" | "success" | "error";

interface Props {
    status: ProcessingStatus;
    errorMsg?: string | null;
}

interface StepItem {
    id: number;
    title: string;
    duration: number; // simulated duration in ms
}

const TIMELINE_STEPS: StepItem[] = [
    { id: 1, title: "Resume Uploaded", duration: 1000 },
    { id: 2, title: "Resume Extracted", duration: 1500 },
    { id: 3, title: "Parsing Resume", duration: 2000 },
    { id: 4, title: "Analyzing Job", duration: 3000 },
    { id: 5, title: "AI Skill Matching", duration: 4000 },
    { id: 6, title: "Saving Application", duration: 2000 },
    { id: 7, title: "Finalizing", duration: 1000 },
];

export default function AIProcessingTimeline({ status, errorMsg }: Props) {
    const [currentStepIndex, setCurrentStepIndex] = useState(0);
    const [completedSteps, setCompletedSteps] = useState<number[]>([]);
    const [progressPercent, setProgressPercent] = useState(0);

    // Simulated progress loop for processing phase
    useEffect(() => {
        if (status !== "processing") return;

        let activeIndex = 0;
        const intervals: ReturnType<typeof setInterval>[] = [];

        const runNextStep = () => {
            if (activeIndex >= TIMELINE_STEPS.length) return;

            setCurrentStepIndex(activeIndex);
            const currentStep = TIMELINE_STEPS[activeIndex];

            // Progress percentage calculation
            const baseProgress = (activeIndex / TIMELINE_STEPS.length) * 100;
            const nextProgress = ((activeIndex + 1) / TIMELINE_STEPS.length) * 100;
            
            // Incremental step progress ticks
            const ticks = 10;
            const tickDuration = currentStep.duration / ticks;
            let tickCount = 0;

            const progressInterval = setInterval(() => {
                tickCount++;
                const incrementalProgress = baseProgress + (tickCount / ticks) * (nextProgress - baseProgress);
                setProgressPercent(Math.min(Math.round(incrementalProgress), 95)); // caps at 95% until complete
                
                if (tickCount >= ticks) {
                    clearInterval(progressInterval);
                    setCompletedSteps((prev) => [...prev, currentStep.id]);
                    activeIndex++;
                    runNextStep();
                }
            }, tickDuration);

            intervals.push(progressInterval);
        };

        runNextStep();

        return () => {
            intervals.forEach((id) => clearInterval(id));
        };
    }, [status]);

    // Handle immediate success resolution
    useEffect(() => {
        if (status === "success") {
            // mark all steps as completed
            setCompletedSteps(TIMELINE_STEPS.map((s) => s.id));
            setCurrentStepIndex(TIMELINE_STEPS.length);
            setProgressPercent(100);
        }
    }, [status]);

    return (
        <div className="flex flex-col items-center justify-center py-6 px-4 max-w-md mx-auto w-full">
            {/* Top Header / Progress Ring / Percentage */}
            <div className="flex flex-col items-center mb-8 text-center">
                <div className="relative flex items-center justify-center h-24 w-24 mb-4">
                    <svg className="w-full h-full transform -rotate-90">
                        <circle
                            cx="48"
                            cy="48"
                            r="42"
                            className="stroke-slate-800"
                            strokeWidth="4"
                            fill="transparent"
                        />
                        <motion.circle
                            cx="48"
                            cy="48"
                            r="42"
                            stroke={status === "error" ? "#ef4444" : status === "success" ? "#10b981" : "#3b82f6"}
                            strokeWidth="4"
                            fill="transparent"
                            strokeDasharray={2 * Math.PI * 42}
                            animate={{
                                strokeDashoffset: 2 * Math.PI * 42 * (1 - progressPercent / 100),
                            }}
                            transition={{ ease: "easeInOut", duration: 0.3 }}
                        />
                    </svg>
                    <div className="absolute text-xl font-bold tracking-tight text-white tabular-nums">
                        {progressPercent}%
                    </div>
                </div>

                <h3 className="text-lg font-bold text-white tracking-tight">
                    {status === "success" ? (
                        <span className="text-emerald-400">Application Created!</span>
                    ) : status === "error" ? (
                        <span className="text-red-400">Processing Failed</span>
                    ) : (
                        "AI is analyzing application..."
                    )}
                </h3>
                <p className="text-xs text-slate-500 mt-1 max-w-[280px]">
                    {status === "success"
                        ? "Success! Loading your new dashboard pipeline..."
                        : status === "error"
                        ? errorMsg || "Something went wrong during analysis."
                        : "This usually takes 10–20 seconds. Please do not close this window."}
                </p>
            </div>

            {/* Steps Timeline Container */}
            <div className="w-full space-y-4 bg-slate-950/20 border border-slate-800/40 rounded-2xl p-5 mb-2">
                {TIMELINE_STEPS.map((step, idx) => {
                    const isCompleted = completedSteps.includes(step.id);
                    const isActive = currentStepIndex === idx && status === "processing";
                    const isPending = !isCompleted && !isActive;

                    return (
                        <div key={step.id} className="flex items-center gap-4 relative">
                            {/* Connector Line */}
                            {idx < TIMELINE_STEPS.length - 1 && (
                                <div className="absolute left-[0.875rem] top-7 bottom-[-1rem] w-[1.5px] bg-slate-800 z-0">
                                    <motion.div
                                        className="w-full bg-emerald-500"
                                        initial={{ height: 0 }}
                                        animate={{ height: isCompleted ? "100%" : 0 }}
                                        transition={{ duration: 0.3 }}
                                    />
                                </div>
                            )}

                            {/* Circle Indicator */}
                            <div className="z-10 relative">
                                <motion.div
                                    initial={{ scale: 0.8 }}
                                    animate={{
                                        scale: isActive ? 1.05 : 1,
                                    }}
                                    className={`flex h-7 w-7 items-center justify-center rounded-full border-2 transition-all duration-300 ${
                                        isCompleted
                                            ? "bg-emerald-500/10 border-emerald-500 text-emerald-400"
                                            : isActive
                                            ? "bg-blue-600/10 border-blue-500 text-blue-400 pulse-glow-blue"
                                            : "bg-slate-900 border-slate-800 text-slate-500"
                                    }`}
                                >
                                    {isCompleted ? (
                                        <Check className="w-3.5 h-3.5 stroke-[3px]" />
                                    ) : isActive ? (
                                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                                    ) : (
                                        <span className="text-[10px] font-bold">{step.id}</span>
                                    )}
                                </motion.div>
                            </div>

                            {/* Step Labels */}
                            <div className="flex flex-col">
                                <span
                                    className={`font-semibold text-xs transition-colors duration-300 ${
                                        isCompleted
                                            ? "text-emerald-400"
                                            : isActive
                                            ? "text-blue-400 font-bold"
                                            : "text-slate-500"
                                    }`}
                                >
                                    {step.title}
                                </span>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
