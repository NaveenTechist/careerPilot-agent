"use client";

import { useState, useEffect } from "react";
import { X, Loader2, CheckCircle2, AlertTriangle, Compass, Play, XCircle, Terminal } from "lucide-react";
import { getApplicationDetails } from "@/services/application";
import { proceedMatch, cancelMatch } from "@/services/matching";
import ScoreCircle from "./ScoreCircle";
import SkillBadge from "./SkillBadge";
import StatusBadge from "./StatusBadge";
import JourneyIndicator from "./JourneyIndicator";
import DrawerSkeleton from "./DrawerSkeleton";

type Props = {
    applicationId: string | null;
    onClose: () => void;
    onStatusChange: () => void;
};

export default function ApplicationDrawer({ applicationId, onClose, onStatusChange }: Props) {
    const [details, setDetails] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [actionLoading, setActionLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isMobile, setIsMobile] = useState(false);

    // Detect mobile viewport size
    useEffect(() => {
        const checkMobile = () => {
            setIsMobile(window.innerWidth < 768);
        };
        checkMobile();
        window.addEventListener("resize", checkMobile);
        return () => window.removeEventListener("resize", checkMobile);
    }, []);

    useEffect(() => {
        if (applicationId) {
            loadDetails(applicationId);
        } else {
            setDetails(null);
        }
    }, [applicationId]);

    async function loadDetails(id: string) {
        setLoading(true);
        setError(null);
        try {
            const data = await getApplicationDetails(id);
            setDetails(data);
        } catch (err: any) {
            setError(err.message || "Failed to load application details.");
        } finally {
            setLoading(false);
        }
    }

    async function handleProceed() {
        if (!details?.match_id) return;
        setActionLoading(true);
        try {
            await proceedMatch(details.match_id);
            onStatusChange();
            if (applicationId) await loadDetails(applicationId);
        } catch (err: any) {
            setError(err.message || "Failed to proceed.");
        } finally {
            setActionLoading(false);
        }
    }

    async function handleCancel() {
        if (!details?.match_id) return;
        setActionLoading(true);
        try {
            await cancelMatch(details.match_id);
            onStatusChange();
            if (applicationId) await loadDetails(applicationId);
        } catch (err: any) {
            setError(err.message || "Failed to cancel.");
        } finally {
            setActionLoading(false);
        }
    }

    if (!applicationId) return null;

    const isProceedDisabled =
        actionLoading ||
        details?.status === "PROCEEDED" ||
        details?.status === "CANCELLED" ||
        details?.status === "COMPLETED" ||
        details?.should_apply === false;

    const isCancelDisabled =
        actionLoading ||
        details?.status === "PROCEEDED" ||
        details?.status === "CANCELLED" ||
        details?.status === "COMPLETED";

    const statusMessage = (() => {
        if (details?.status === "CANCELLED") return "Application Cancelled";
        if (details?.status === "PROCEEDED") return "Automation Started";
        if (details?.status === "COMPLETED") return "Application Submitted";
        return null;
    })();

    // Panel styling class based on layout mode
    const panelClass = isMobile
        ? "fixed bottom-0 left-0 right-0 z-50 w-full bg-slate-950 border-t border-slate-800 shadow-2xl flex flex-col overflow-hidden animate-slide-in-bottom bottom-sheet max-h-[88vh]"
        : "fixed inset-y-0 right-0 z-50 w-full max-w-xl bg-slate-950 border-l border-slate-800 shadow-2xl flex flex-col overflow-hidden animate-slide-in-drawer";

    return (
        <>
            {/* Backdrop */}
            <div
                className="fixed inset-0 z-40 bg-slate-950/60 backdrop-blur-sm transition-opacity"
                onClick={onClose}
            />

            {/* Panel */}
            <div className={panelClass}>
                
                {/* Mobile Drag Indicator Bar */}
                {isMobile && (
                    <div className="w-12 h-1.5 bg-slate-800 rounded-full mx-auto mt-3 shrink-0" />
                )}

                {/* Header */}
                <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800/80 shrink-0">
                    <h3 className="text-sm font-bold text-white tracking-widest uppercase">
                        Application Details
                    </h3>
                    <button
                        onClick={onClose}
                        className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white transition-colors cursor-pointer"
                        aria-label="Close details"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Panel Content */}
                <div className="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-6">
                    {loading && <DrawerSkeleton />}

                    {error && !loading && (
                        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
                            {error}
                        </div>
                    )}

                    {details && !loading && (
                        <>
                            {/* Title + Status */}
                            <div className="flex items-start justify-between gap-3">
                                <div>
                                    <h2 className="text-lg font-bold text-white leading-snug">{details.title}</h2>
                                    <p className="text-[10px] text-slate-500 mt-1 uppercase font-semibold tracking-wider">
                                        ID: {details.id}
                                    </p>
                                </div>
                                <StatusBadge status={details.status} />
                            </div>

                            {/* Status Banner */}
                            {statusMessage && (
                                <div className={`p-3.5 rounded-xl text-xs font-semibold border ${
                                    details.status === "CANCELLED"
                                        ? "bg-red-500/10 border-red-500/20 text-red-400"
                                        : details.status === "COMPLETED"
                                            ? "bg-purple-500/10 border-purple-500/20 text-purple-400"
                                            : "bg-emerald-500/10 border-emerald-500/20 text-emerald-400"
                                }`}>
                                    {statusMessage}
                                </div>
                            )}

                            {/* Score circular graphic */}
                            <div className="flex justify-center py-2">
                                <ScoreCircle
                                    score={details.score || 0}
                                    level={details.overall_level ? `${details.overall_level} Match` : "Match Score"}
                                />
                            </div>

                            {/* Journey Timeline */}
                            <div className="space-y-3 bg-slate-950/20 border border-slate-800/40 rounded-2xl p-5">
                                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                                    Application Pipeline Journey
                                </h4>
                                <JourneyIndicator status={details.status} layout="vertical" />
                            </div>

                            {/* Recommendation */}
                            {details.recommendation && (
                                <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 space-y-2">
                                    <h4 className="text-xs font-bold text-blue-400 uppercase tracking-widest flex items-center gap-1.5">
                                        <Compass className="w-3.5 h-3.5" />
                                        Recommendation
                                    </h4>
                                    <p className="text-sm text-slate-300 leading-relaxed">
                                        {details.recommendation}
                                    </p>
                                </div>
                            )}

                            {/* Matched Skills */}
                            {details.matched_skills && details.matched_skills.length > 0 && (
                                <div className="space-y-3">
                                    <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-widest flex items-center gap-1.5">
                                        <CheckCircle2 className="w-3.5 h-3.5" />
                                        Matched Skills ({details.matched_skills.length})
                                    </h4>
                                    <div className="flex flex-wrap gap-2">
                                        {details.matched_skills.map((s: string) => (
                                            <SkillBadge key={s} text={s} type="success" />
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Missing Skills */}
                            {details.missing_skills && details.missing_skills.length > 0 && (
                                <div className="space-y-3">
                                    <h4 className="text-xs font-bold text-amber-400 uppercase tracking-widest flex items-center gap-1.5">
                                        <AlertTriangle className="w-3.5 h-3.5" />
                                        Missing Skills ({details.missing_skills.length})
                                    </h4>
                                    <div className="flex flex-wrap gap-2">
                                        {details.missing_skills.map((s: string) => (
                                            <SkillBadge key={s} text={s} type="warning" />
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Strengths */}
                            {details.strengths && details.strengths.length > 0 && (
                                <div className="space-y-3">
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1.5">
                                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                                        Strengths
                                    </h4>
                                    <ul className="space-y-1.5">
                                        {details.strengths.map((s: string, i: number) => (
                                            <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                                                <span className="text-emerald-500 font-bold shrink-0">✓</span>
                                                {s}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {/* Weaknesses */}
                            {details.weaknesses && details.weaknesses.length > 0 && (
                                <div className="space-y-3">
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1.5">
                                        <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
                                        Weaknesses
                                    </h4>
                                    <ul className="space-y-1.5">
                                        {details.weaknesses.map((s: string, i: number) => (
                                            <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                                                <span className="text-amber-500 font-bold shrink-0">!</span>
                                                {s}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {/* Resume Summary */}
                            {details.resume_summary && (
                                <div className="space-y-2">
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                                        Resume Summary
                                    </h4>
                                    <p className="text-sm text-slate-300 leading-relaxed">
                                        {details.resume_summary}
                                    </p>
                                </div>
                            )}

                            {/* Job Summary */}
                            {details.job_summary && (
                                <div className="space-y-2">
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                                        Job Summary
                                    </h4>
                                    <p className="text-sm text-slate-300 leading-relaxed">
                                        {details.job_summary}
                                    </p>
                                </div>
                            )}

                            {/* Next Steps */}
                            {details.next_steps && details.next_steps.length > 0 && (
                                <div className="space-y-2">
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                                        Next Steps
                                    </h4>
                                    <ul className="space-y-1.5">
                                        {details.next_steps.map((s: string, i: number) => (
                                            <li key={i} className="text-xs text-slate-400 flex items-center gap-2">
                                                <span className="h-1.5 w-1.5 rounded-full bg-blue-500 shrink-0" />
                                                {s}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {/* Automation Log */}
                            <div className="space-y-3 opacity-60">
                                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-1.5">
                                    <Terminal className="w-3.5 h-3.5" />
                                    Automation Logs
                                </h4>
                                <div className="rounded-xl border border-slate-900 bg-slate-950/40 p-4 text-[11px] font-mono text-slate-500 select-none">
                                    // [SYSTEM] Job Application Agent is offline.
                                    <br />
                                    // Waiting for matching confirmation to trigger background process logs...
                                    <br />
                                    // (Feature coming soon)
                                </div>
                            </div>
                        </>
                    )}
                </div>

                {/* Footer Actions */}
                {details && !loading && (
                    <div className="px-6 py-4 border-t border-slate-800/80 bg-slate-950/80 flex justify-end gap-3 shrink-0">
                        <button
                            onClick={handleCancel}
                            disabled={isCancelDisabled}
                            className="inline-flex items-center gap-2 rounded-xl border border-red-550/30 bg-transparent px-5 py-2.5 text-xs font-bold text-red-400 hover:bg-red-500/10 disabled:opacity-40 disabled:cursor-not-allowed transition-all cursor-pointer"
                        >
                            {actionLoading ? (
                                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                            ) : (
                                <XCircle className="w-3.5 h-3.5" />
                            )}
                            Cancel Match
                        </button>
                        <button
                            onClick={handleProceed}
                            disabled={isProceedDisabled}
                            className="inline-flex items-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 disabled:text-slate-500 px-6 py-2.5 text-xs font-bold text-white transition-all disabled:cursor-not-allowed cursor-pointer"
                        >
                            {actionLoading ? (
                                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                            ) : (
                                <Play className="w-3.5 h-3.5 fill-current" />
                            )}
                            Proceed Application
                        </button>
                    </div>
                )}
            </div>
        </>
    );
}
