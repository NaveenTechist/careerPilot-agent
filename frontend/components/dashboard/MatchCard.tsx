"use client";

import { useEffect, useRef } from "react";
import ScoreCircle from "./ScoreCircle";
import SkillBadge from "./SkillBadge";
import ActionButtons from "./ActionButtons";
import { 
    Sparkles, 
    CheckCircle2, 
    XCircle, 
    PlusCircle, 
    TrendingUp, 
    Info, 
    AlertTriangle,
    ShieldCheck,
    Compass
} from "lucide-react";

type Props = {
    result: any;
    onProceed: () => void;
    onCancel: () => void;
};

export default function MatchCard({
    result,
    onProceed,
    onCancel,
}: Props) {
    const cardRef = useRef<HTMLDivElement>(null);

    // Scroll to the card when event is received
    useEffect(() => {
        const handleScrollToMatch = () => {
            if (cardRef.current) {
                cardRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        };
        window.addEventListener("scroll-to-match", handleScrollToMatch);
        return () => window.removeEventListener("scroll-to-match", handleScrollToMatch);
    }, []);

    if (!result) return null;

    const matchedCount = result.matched_skills?.length || 0;
    const missingCount = result.missing_skills?.length || 0;
    const totalSkills = matchedCount + missingCount;
    const matchedRatio = totalSkills > 0 ? (matchedCount / totalSkills) * 100 : 0;
    const missingRatio = totalSkills > 0 ? (missingCount / totalSkills) * 100 : 0;

    return (
        <div 
            ref={cardRef}
            id="match-results-section" 
            className="premium-card p-6 md:p-8 shadow-2xl transition-all duration-300 border-l-4 border-l-blue-500 scroll-mt-24"
        >
            {/* Top Row: Title info & Score ring */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-900/60">
                <div className="flex items-center gap-3">
                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-600/10 text-blue-400">
                        <Sparkles className="w-5 h-5" />
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-white tracking-tight">
                            Match Results
                        </h2>
                        <p className="text-xs text-slate-400 mt-1">
                            AI compared your profile with job details
                        </p>
                    </div>
                </div>

                <div className="flex justify-start md:justify-end">
                    <ScoreCircle score={result.score} level={result.overall_level ? `${result.overall_level} Match` : "Excellent Match"} />
                </div>
            </div>

            {/* Middle Grid: Skills Progress & Lists */}
            <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Matched Skills */}
                <div className="space-y-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <span className="h-2 w-2 rounded-full bg-emerald-500" />
                            <h3 className="font-bold text-sm text-emerald-400 uppercase tracking-wider">
                                Matched Skills
                            </h3>
                        </div>
                        <span className="text-xs font-semibold text-slate-400">
                            {matchedCount} / {totalSkills}
                        </span>
                    </div>

                    {/* Progress Bar */}
                    <div className="w-full h-2 rounded-full bg-slate-950 overflow-hidden border border-slate-900">
                        <div 
                            className="h-full bg-gradient-to-r from-emerald-600 to-emerald-400 rounded-full transition-all duration-1000"
                            style={{ width: `${matchedRatio}%` }}
                        />
                    </div>

                    <div className="flex flex-wrap gap-2 pt-2 max-h-[140px] overflow-y-auto custom-scrollbar">
                        {result.matched_skills && result.matched_skills.length > 0 ? (
                            result.matched_skills.map((skill: string) => (
                                <SkillBadge
                                    key={skill}
                                    text={skill}
                                    type="success"
                                />
                            ))
                        ) : (
                            <span className="text-xs text-slate-500 italic">No matching skills found</span>
                        )}
                    </div>
                </div>

                {/* Missing Skills */}
                <div className="space-y-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <span className="h-2 w-2 rounded-full bg-amber-500" />
                            <h3 className="font-bold text-sm text-amber-400 uppercase tracking-wider">
                                Missing Skills
                            </h3>
                        </div>
                        <span className="text-xs font-semibold text-slate-400">
                            {missingCount} / {totalSkills}
                        </span>
                    </div>

                    {/* Progress Bar */}
                    <div className="w-full h-2 rounded-full bg-slate-950 overflow-hidden border border-slate-900">
                        <div 
                            className="h-full bg-gradient-to-r from-amber-600 to-amber-400 rounded-full transition-all duration-1000"
                            style={{ width: `${missingRatio}%` }}
                        />
                    </div>

                    <div className="flex flex-wrap gap-2 pt-2 max-h-[140px] overflow-y-auto custom-scrollbar">
                        {result.missing_skills && result.missing_skills.length > 0 ? (
                            result.missing_skills.map((skill: string) => (
                                <SkillBadge
                                    key={skill}
                                    text={skill}
                                    type="warning"
                                />
                            ))
                        ) : (
                            <span className="text-xs text-emerald-500 font-semibold italic flex items-center gap-1">
                                <CheckCircle2 className="w-3.5 h-3.5" /> No missing skills!
                            </span>
                        )}
                    </div>
                </div>
            </div>

            {/* Strengths & Weaknesses (AI Analysis) */}
            <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6 pt-6 border-t border-slate-900/65">
                {/* Strengths */}
                <div className="space-y-3">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                        Top Strengths
                    </h4>
                    <ul className="space-y-2">
                        {result.strengths && result.strengths.length > 0 ? (
                            result.strengths.map((str: string, idx: number) => (
                                <li key={idx} className="text-sm text-slate-300 flex items-start gap-2 leading-relaxed">
                                    <span className="text-emerald-500 font-bold shrink-0 select-none">✓</span>
                                    <span>{str}</span>
                                </li>
                            ))
                        ) : (
                            <li className="text-xs text-slate-500 italic">No major strengths analyzed.</li>
                        )}
                    </ul>
                </div>

                {/* Weaknesses / Risks */}
                <div className="space-y-3">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1.5">
                        <AlertTriangle className="w-4 h-4 text-amber-500" />
                        Potential Gaps
                    </h4>
                    <ul className="space-y-2">
                        {result.weaknesses && result.weaknesses.length > 0 ? (
                            result.weaknesses.map((weak: string, idx: number) => (
                                <li key={idx} className="text-sm text-slate-300 flex items-start gap-2 leading-relaxed">
                                    <span className="text-amber-500 font-bold shrink-0 select-none">!</span>
                                    <span>{weak}</span>
                                </li>
                            ))
                        ) : (
                            <li className="text-xs text-slate-500 italic">No critical gaps identified.</li>
                        )}
                    </ul>
                </div>
            </div>

            {/* Recommendation & Next steps */}
            <div className="mt-8 p-4 md:p-5 rounded-xl bg-slate-900/40 border border-slate-850 space-y-4">
                <div className="space-y-2">
                    <h4 className="text-xs font-bold text-blue-400 uppercase tracking-widest flex items-center gap-1.5">
                        <Compass className="w-4 h-4" />
                        Recommendations
                    </h4>
                    <p className="text-sm text-slate-300 leading-relaxed font-sans">
                        {result.recommendation}
                    </p>
                </div>

                {result.next_steps && result.next_steps.length > 0 && (
                    <div className="pt-2.5 border-t border-slate-900/60">
                        <h5 className="text-xs font-semibold text-slate-400">Next Steps:</h5>
                        <ul className="mt-2 space-y-1.5">
                            {result.next_steps.map((step: string, idx: number) => (
                                <li key={idx} className="text-xs text-slate-400 flex items-center gap-2">
                                    <span className="h-1 w-1 rounded-full bg-blue-500 shrink-0" />
                                    {step}
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>

            {/* Action Buttons */}
            <ActionButtons
                matchId={result.match_id}
                shouldApply={result.should_apply}
                onProceed={onProceed}
                onCancel={onCancel}
            />
        </div>
    );
}