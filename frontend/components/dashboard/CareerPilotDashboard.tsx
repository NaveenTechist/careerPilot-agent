"use client";

import { useEffect, useState } from "react";
import ResumeCard from "./ResumeCard";
import JobCard from "./JobCard";
import MatchCard from "./MatchCard";
import ProgressStepper from "./ProgressStepper";
import Header from "./Header";
import Notification from "./Notification";

import { getSession } from "@/services/session";
import { uploadResume } from "@/services/resume";
import { analyzeJob } from "@/services/job";
import {
    getCurrentMatch,
    matchResume,
    proceedMatch,
    cancelMatch,
} from "@/services/matching";

import { useNotification } from "@/hooks/useNotification";
import {
    Bot,
    Sparkles,
    Cpu,
    Zap,
    Shield,
    BarChart3,
    ArrowRight,
    Loader2
} from "lucide-react";

export default function CareerPilotDashboard() {
    const [session, setSession] = useState<any>(null);
    const [match, setMatch] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [automationStarted, setAutomationStarted] = useState(false);


    const { notify, message, open, dismiss } = useNotification();

    async function refreshSession() {
        try {
            const data = await getSession();
            setSession(data);
        } catch (e: any) {
            console.error("Failed to load session:", e);
        }
    }

    useEffect(() => {

        loadSession();
        loadCurrentMatch();

    }, []);

    useEffect(() => {
        refreshSession();
    }, []);

    // Listen for custom trigger from command palette to start matching
    useEffect(() => {
        const handleMatchTrigger = () => {
            if (session?.status === "READY_FOR_MATCHING" && !loading) {
                handleMatch();
            }
        };
        window.addEventListener("trigger-match-analysis", handleMatchTrigger);
        return () => window.removeEventListener("trigger-match-analysis", handleMatchTrigger);
    }, [session, loading]);

    // Listen to custom alert settings trigger from Command Palette
    useEffect(() => {
        const handleSettingsAlert = () => {
            notify("Settings navigation will be integrated in future release.");
        };
        window.addEventListener("show-settings-alert", handleSettingsAlert);
        return () => window.removeEventListener("show-settings-alert", handleSettingsAlert);
    }, []);

    async function loadCurrentMatch() {
        try {
            const response = await getCurrentMatch();
            if (
                response.data.exists
            ) {
                setMatch(
                    response.data.match
                );
            }
        }
        catch {
        }
    }

    async function loadSession() {
        const response = await getSession();
        setSession(response.data);
    }

    async function handleResume(file: File) {
        setLoading(true);
        try {
            await uploadResume(file);
            notify("Resume uploaded successfully.");
            await refreshSession();
        } catch (e: any) {
            notify(e.message || "Failed to upload resume.");
        } finally {
            setLoading(false);
        }
    }

    async function handleJob(url: string) {
        setLoading(true);
        try {
            await analyzeJob(url);
            notify("Job analyzed successfully.");
            await refreshSession();
        } catch (e: any) {
            notify(e.message || "Failed to analyze job.");
        } finally {
            setLoading(false);
        }
    }

    async function handleMatch() {
        setLoading(true);
        try {
            const result = await matchResume();
            setMatch(result);
            notify("Matching completed.");
            // Scroll to results automatically
            setTimeout(() => {
                window.dispatchEvent(new CustomEvent("scroll-to-match"));
            }, 300);
        } catch (e: any) {
            notify(e.message || "Matching evaluation failed.");
        } finally {
            setLoading(false);
        }
    }

    async function handleProceed() {
        setAutomationStarted(true);
        try {
            await proceedMatch(match.match_id);
            notify("Browser automation started.");
            await refreshSession();
        } catch (e: any) {
            notify(e.message || "Automation failed to start.");
            setAutomationStarted(false);
        }
    }

    async function handleCancel() {
        try {
            await cancelMatch(match.match_id);
            notify("Application cancelled.");
            setMatch(null);
            setAutomationStarted(false);
            await refreshSession();
        } catch (e: any) {
            notify(e.message || "Cancellation failed.");
        }
    }

    return (
        <main className="min-h-screen bg-[#020617] text-[#f8fafc] flex flex-col">
            <Header />
            <Notification open={open} message={message} onClose={dismiss} />

            <div className="flex-1 mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8 space-y-10">

                {/* 1. Progress workflow stepper */}
                <ProgressStepper
                    session={session}
                    match={match}
                    automationStarted={automationStarted}
                />

                {/* 2. Main uploaders grid */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <ResumeCard session={session} onUpload={handleResume} />
                    <JobCard session={session} onAnalyze={handleJob} />
                </div>

                {/* 3. Ready to Match Hero banner */}
                {session?.status === "READY_FOR_MATCHING" && !match && (
                    <div className="w-full premium-card p-6 md:p-8 bg-gradient-to-r from-blue-950/20 via-slate-900/40 to-purple-950/20 border border-blue-500/25 flex flex-col md:flex-row items-center justify-between gap-6 shadow-[0_0_30px_rgba(59,130,246,0.08)]">
                        <div className="flex items-center gap-4.5 text-left">
                            <div className="relative flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-purple-600 text-white shadow-lg shadow-blue-950/50">
                                <Bot className="w-6.5 h-6.5 animate-pulse" />
                                <span className="absolute -top-1 -right-1 flex h-3 w-3 rounded-full bg-emerald-500 ring-2 ring-slate-950" />
                            </div>
                            <div>
                                <h3 className="text-base md:text-lg font-bold text-white tracking-tight">
                                    Ready to analyze your match?
                                </h3>
                                <p className="text-xs md:text-sm text-slate-400 mt-1">
                                    Our AI will compare your profile with the job requirements and identify gaps.
                                </p>
                            </div>
                        </div>

                        <button
                            onClick={handleMatch}
                            disabled={loading}
                            className="w-full md:w-auto inline-flex items-center justify-center gap-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-3.5 font-bold text-white shadow-lg shadow-blue-950/45 hover:from-blue-500 hover:to-indigo-500 transition-all duration-200 active:translate-y-0.5 disabled:opacity-60 disabled:cursor-not-allowed group text-sm shrink-0"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                    Analyzing Match...
                                </>
                            ) : (
                                <>
                                    <Sparkles className="w-4 h-4 text-blue-200 group-hover:rotate-12 transition-transform" />
                                    Analyze Resume Match
                                </>
                            )}
                        </button>
                    </div>
                )}

                {/* 4. Match analysis card */}
                {match && (
                    <MatchCard
                        result={match}
                        onProceed={handleProceed}
                        onCancel={handleCancel}
                    />
                )}

                {/* 5. Premium Platform value features footer grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 pt-6 border-t border-slate-900">
                    <div className="premium-card p-5 flex flex-col justify-between">
                        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600/10 text-blue-400">
                            <Cpu className="w-5 h-5" />
                        </div>
                        <div className="mt-4">
                            <h4 className="text-sm font-bold text-slate-100">AI-Powered Matching</h4>
                            <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">
                                Advanced AI algorithms compare resumes and jobs to find key compatible areas.
                            </p>
                        </div>
                    </div>

                    <div className="premium-card p-5 flex flex-col justify-between">
                        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600/10 text-indigo-400">
                            <Zap className="w-5 h-5" />
                        </div>
                        <div className="mt-4">
                            <h4 className="text-sm font-bold text-slate-100">Smart Automation</h4>
                            <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">
                                Auto-fill applications on target platforms and save 10+ hours weekly.
                            </p>
                        </div>
                    </div>

                    <div className="premium-card p-5 flex flex-col justify-between">
                        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-600/10 text-emerald-400">
                            <Shield className="w-5 h-5" />
                        </div>
                        <div className="mt-4">
                            <h4 className="text-sm font-bold text-slate-100">Secure & Private</h4>
                            <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">
                                Your career data is fully encrypted and kept 100% confidential.
                            </p>
                        </div>
                    </div>

                    <div className="premium-card p-5 flex flex-col justify-between">
                        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-600/10 text-purple-400">
                            <BarChart3 className="w-5 h-5" />
                        </div>
                        <div className="mt-4">
                            <h4 className="text-sm font-bold text-slate-100">Track Progress</h4>
                            <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">
                                Get live status notifications for your automation pipeline.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
}