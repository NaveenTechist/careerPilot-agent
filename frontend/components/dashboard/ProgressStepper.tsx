"use client";

import { Check, Loader2, Sparkles, FileText, Link2, Play } from "lucide-react";

interface Props {
    session: any;
    match?: any;
    automationStarted?: boolean;
}

export default function ProgressStepper({ session, match, automationStarted = false }: Props) {
    const isResumeUploaded = !!session?.resume?.uploaded;
    const isJobUploaded = !!session?.job?.uploaded;
    const isMatchAnalyzed = !!match;
    const isAutomationActive = automationStarted || session?.status === "PROCEEDED";

    // Step Status determination: "completed" | "current" | "pending"
    const getStepStatus = (index: number) => {
        if (index === 0) {
            return isResumeUploaded ? "completed" : "current";
        }
        if (index === 1) {
            if (isJobUploaded) return "completed";
            return isResumeUploaded ? "current" : "pending";
        }
        if (index === 2) {
            if (isMatchAnalyzed) return "completed";
            return (isResumeUploaded && isJobUploaded) ? "current" : "pending";
        }
        if (index === 3) {
            if (isAutomationActive) return "completed";
            return isMatchAnalyzed ? "current" : "pending";
        }
        return "pending";
    };

    const steps = [
        {
            title: "Resume Uploaded",
            desc: isResumeUploaded ? "Completed" : "Upload your resume",
            icon: <FileText className="w-5 h-5" />,
        },
        {
            title: "Job Analyzed",
            desc: isJobUploaded ? "Completed" : "Analyze target job URL",
            icon: <Link2 className="w-5 h-5" />,
        },
        {
            title: "Match Analysis",
            desc: isMatchAnalyzed ? "Completed" : (isJobUploaded && isResumeUploaded) ? "In Progress" : "Pending",
            icon: <Sparkles className="w-5 h-5" />,
        },
        {
            title: "Automation",
            desc: isAutomationActive ? "Running" : "Pending",
            icon: <Play className="w-5 h-5" />,
        },
    ];

    return (
        <div className="w-full premium-card p-6 md:p-8">
            {/* Desktop Stepper (Horizontal) */}
            <div className="hidden md:flex items-center justify-between relative">
                {steps.map((step, idx) => {
                    const status = getStepStatus(idx);
                    
                    return (
                        <div key={idx} className="flex-1 flex items-center relative">
                            {/* Connector Line */}
                            {idx < steps.length - 1 && (
                                <div className="absolute left-[2.5rem] right-0 top-1/2 -translate-y-1/2 h-[2px] bg-slate-800 z-0">
                                    <div 
                                        className={`h-full bg-gradient-to-r from-emerald-500 to-blue-500 transition-all duration-500 ${
                                            getStepStatus(idx + 1) === "completed" 
                                                ? "w-full" 
                                                : getStepStatus(idx + 1) === "current" 
                                                    ? "w-1/2" 
                                                    : "w-0"
                                        }`}
                                    />
                                </div>
                            )}

                            {/* Step Item */}
                            <div className="flex items-center gap-4 z-10 relative bg-[#0f172a] pr-4">
                                {/* Icon container */}
                                <div className={`relative flex h-12 w-12 items-center justify-center rounded-full border-2 transition-all duration-300 ${
                                    status === "completed"
                                        ? "bg-emerald-500/10 border-emerald-500 text-emerald-400"
                                        : status === "current"
                                            ? "bg-blue-600/10 border-blue-500 text-blue-400 shadow-[0_0_15px_rgba(59,130,246,0.3)] pulse-primary"
                                            : "bg-slate-900 border-slate-800 text-slate-500"
                                }`}>
                                    {status === "completed" ? (
                                        <Check className="w-5 h-5 stroke-[3px]" />
                                    ) : status === "current" && idx === 2 ? (
                                        <Loader2 className="w-5 h-5 animate-spin" />
                                    ) : (
                                        step.icon
                                    )}

                                    {/* Number label for non-completed steps if wanted, or just icon */}
                                </div>

                                {/* Step labels */}
                                <div className="flex flex-col">
                                    <span className={`font-semibold text-sm leading-snug ${
                                        status === "completed"
                                            ? "text-emerald-400"
                                            : status === "current"
                                                ? "text-blue-400"
                                                : "text-slate-500"
                                    }`}>
                                        {step.title}
                                    </span>
                                    <span className="text-xs text-slate-400 mt-0.5">
                                        {step.desc}
                                    </span>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Mobile Stepper (Vertical Timeline) */}
            <div className="md:hidden flex flex-col gap-6 relative">
                {steps.map((step, idx) => {
                    const status = getStepStatus(idx);

                    return (
                        <div key={idx} className="flex gap-4 relative">
                            {/* Vertical Line */}
                            {idx < steps.length - 1 && (
                                <div className="absolute left-6 top-12 bottom-[-1.5rem] w-[2px] bg-slate-800 z-0">
                                    <div 
                                        className={`w-full bg-gradient-to-b from-emerald-500 to-blue-500 transition-all duration-500 ${
                                            getStepStatus(idx + 1) === "completed"
                                                ? "h-full"
                                                : getStepStatus(idx + 1) === "current"
                                                    ? "h-1/2"
                                                    : "h-0"
                                        }`}
                                    />
                                </div>
                            )}

                            {/* Circle Icon */}
                            <div className={`relative flex h-12 w-12 shrink-0 items-center justify-center rounded-full border-2 z-10 ${
                                status === "completed"
                                    ? "bg-emerald-500/10 border-emerald-500 text-emerald-400"
                                    : status === "current"
                                        ? "bg-blue-600/10 border-blue-500 text-blue-400 shadow-[0_0_12px_rgba(59,130,246,0.35)]"
                                        : "bg-slate-900 border-slate-800 text-slate-500"
                            }`}>
                                {status === "completed" ? (
                                    <Check className="w-5 h-5 stroke-[3px]" />
                                ) : status === "current" && idx === 2 ? (
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                ) : (
                                    step.icon
                                )}
                            </div>

                            {/* Labels */}
                            <div className="flex flex-col justify-center">
                                <span className={`font-semibold text-sm leading-snug ${
                                    status === "completed"
                                        ? "text-emerald-400"
                                        : status === "current"
                                            ? "text-blue-400"
                                            : "text-slate-500"
                                }`}>
                                    {step.title}
                                </span>
                                <span className="text-xs text-slate-400 mt-1">
                                    {step.desc}
                                </span>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}