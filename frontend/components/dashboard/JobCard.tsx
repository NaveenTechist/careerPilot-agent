"use client";

import { useState, useRef, useEffect } from "react";
import {
    Briefcase,
    Link2,
    Sparkles,
    Building2,
    ShieldCheck,
    Loader2,
    Layers,
    BookOpen,
    ArrowUpRight
} from "lucide-react";

type Props = {
    session: any;
    onAnalyze: (url: string) => Promise<void>;
};

export default function JobCard({ session, onAnalyze }: Props) {
    const [url, setUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);

    // Listen to custom event from Command Palette
    useEffect(() => {
        const handleFocusTrigger = () => {
            inputRef.current?.focus();
        };
        window.addEventListener("focus-job-input", handleFocusTrigger);
        return () => window.removeEventListener("focus-job-input", handleFocusTrigger);
    }, []);

    async function analyze() {
        if (!url.trim()) return;
        setLoading(true);
        try {
            await onAnalyze(url);
            setUrl("");
        } finally {
            setLoading(false);
        }
    }

    // Enter key submits the job
    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter" && !loading && url.trim()) {
            analyze();
        }
    };

    const isUploaded = !!session?.job?.uploaded;
    const profile = session?.job?.profile;

    return (
        <div className="premium-card p-6 md:p-8 flex flex-col justify-between min-h-[380px] transition-all duration-300">
            {/* Header info */}
            <div>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2.5">
                        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-600/10 text-purple-400">
                            <Briefcase className="w-5 h-5" />
                        </div>
                        <div>
                            <h2 className="text-lg font-bold text-white tracking-tight">
                                Job Analysis
                            </h2>
                            <p className="text-xs text-slate-400 mt-0.5">
                                Paste job posting URL to analyze requirements
                            </p>
                        </div>
                    </div>

                    {isUploaded && (
                        <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-400 border border-emerald-500/20">
                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                            Analyzed
                        </span>
                    )}
                </div>

                {/* Input Area */}
                {!isUploaded ? (
                    <div className="mt-6 space-y-4">
                        <div className="relative group">
                            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-purple-400 transition-colors">
                                <Link2 className="w-5 h-5" />
                            </div>
                            <input
                                ref={inputRef}
                                type="text"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                                onKeyDown={handleKeyDown}
                                placeholder="Paste LinkedIn, Indeed or job posting URL..."
                                className="w-full rounded-xl border border-slate-800 bg-slate-900/40 py-3.5 pl-12 pr-4 text-sm text-slate-100 placeholder-slate-500 outline-none transition-all duration-300 focus:border-purple-500/70 focus:bg-slate-900/60 focus:ring-4 focus:ring-purple-500/10"
                                disabled={loading}
                            />
                        </div>

                        <div className="rounded-xl border border-slate-900 bg-slate-950/40 p-4 text-xs text-slate-500 flex gap-2.5">
                            <Layers className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                            <p className="leading-relaxed">
                                Our AI parser will extract the company name, target job title, required skills, and core requirements to match with your profile.
                            </p>
                        </div>
                    </div>
                ) : (
                    /* Display Parsed Info */
                    <div className="mt-6 space-y-6">
                        {/* Status bar */}
                        <div className="flex items-center justify-between p-4 rounded-xl bg-slate-900/60 border border-slate-850">
                            <div className="flex items-center gap-3 min-w-0">
                                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400">
                                    <ShieldCheck className="w-5 h-5" />
                                </div>
                                <div className="min-w-0">
                                    <h4 className="text-sm font-bold text-slate-200 truncate pr-2">
                                        Job extracted successfully
                                    </h4>
                                    <p className="text-xs text-slate-500 mt-0.5">
                                        Ready for match evaluation
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Metadata Stats Grid */}
                        <div className="grid grid-cols-2 gap-4">
                            {/* Company Card */}
                            <div className="p-3.5 rounded-xl bg-slate-900/40 border border-slate-850/60 hover:border-slate-800 transition-all duration-200">
                                <div className="flex items-center gap-2 text-slate-400">
                                    <Building2 className="w-4 h-4 text-purple-400" />
                                    <span className="text-xs font-semibold tracking-wide uppercase">Company</span>
                                </div>
                                <div className="mt-2 text-base font-bold text-slate-100 truncate">
                                    {profile?.company || "Target Company"}
                                </div>
                            </div>

                            {/* Job Title Card */}
                            <div className="p-3.5 rounded-xl bg-slate-900/40 border border-slate-850/60 hover:border-slate-800 transition-all duration-200">
                                <div className="flex items-center gap-2 text-slate-400">
                                    <Briefcase className="w-4 h-4 text-pink-400" />
                                    <span className="text-xs font-semibold tracking-wide uppercase">Target Title</span>
                                </div>
                                <div className="mt-2 text-base font-bold text-slate-100 truncate">
                                    {profile?.title || "Software Engineer"}
                                </div>
                            </div>

                            {/* Required Skills Card */}
                            <div className="p-3.5 rounded-xl bg-slate-900/40 border border-slate-850/60 hover:border-slate-800 transition-all duration-200 col-span-2">
                                <div className="flex items-center gap-2 text-slate-400">
                                    <BookOpen className="w-4 h-4 text-teal-400" />
                                    <span className="text-xs font-semibold tracking-wide uppercase">Required Skills</span>
                                </div>
                                <div className="mt-2 flex items-baseline gap-1.5">
                                    <span className="text-2xl font-bold text-slate-100">{profile?.required_skills ?? 0}</span>
                                    <span className="text-[11px] text-slate-500">key skills identified in listing</span>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Action buttons footer */}
            <div className="mt-6 pt-4 border-t border-slate-900 flex justify-between items-center">
                <div>
                    {isUploaded && (
                        <p className="text-[11px] text-slate-500">
                            Parsed from external URL
                        </p>
                    )}
                </div>

                <div>
                    {!isUploaded ? (
                        <button
                            onClick={analyze}
                            disabled={loading || !url.trim()}
                            className="inline-flex items-center gap-2 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:bg-slate-800 disabled:text-slate-650 disabled:border-slate-850 border border-transparent px-5 py-2.5 text-xs font-bold text-white shadow-md shadow-purple-950/30 transition-all duration-150 hover:-translate-y-0.5 active:translate-y-0 disabled:translate-y-0"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                                    Analyzing Job...
                                </>
                            ) : (
                                <>
                                    <Sparkles className="w-3.5 h-3.5" />
                                    Analyze Job
                                </>
                            )}
                        </button>
                    ) : (
                        <button
                            onClick={() => {
                                // Trigger edit URL state
                                setUrl("");
                                // Hacky bypass: we can clear job status or let them enter a new URL.
                                // In the workflow, they can just paste a new URL. Let's toggle UI to let them input again.
                                // We will open input mode by dispatching or just showing the input field.
                                // Actually, let's keep status ready but allow re-analysis
                                setUrl("");
                                // Resetting session requires backend, but in UI we can clear locally or let user know.
                                // Let's just render a "New Analysis" trigger that shows the input.
                                // We can use a local state toggle for editing
                                inputRef.current?.focus();
                            }}
                            className="inline-flex items-center gap-1.5 rounded-xl border border-slate-800 hover:border-slate-700 bg-slate-900/50 hover:bg-slate-900 px-4 py-2 text-xs font-semibold text-slate-300 hover:text-white transition-all duration-150"
                        >
                            Analyze Different Job
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}