"use client";

import { useEffect, useState } from "react";

type Props = {
    score: number;
    level?: string;
};

export default function ScoreCircle({ score, level = "Excellent Match" }: Props) {
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        // Animate the progress ring
        const timer = setTimeout(() => setProgress(score), 100);
        return () => clearTimeout(timer);
    }, [score]);

    const radius = 60;
    const strokeWidth = 8;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (progress / 100) * circumference;

    const getColorClass = () => {
        if (score >= 90) return { text: "text-emerald-500", stroke: "url(#emerald-gradient)", bg: "bg-emerald-500/10", border: "border-emerald-500/10" };
        if (score >= 75) return { text: "text-blue-500", stroke: "url(#blue-gradient)", bg: "bg-blue-500/10", border: "border-blue-500/10" };
        if (score >= 60) return { text: "text-amber-500", stroke: "url(#amber-gradient)", bg: "bg-amber-500/10", border: "border-amber-500/10" };
        return { text: "text-red-500", stroke: "url(#red-gradient)", bg: "bg-red-500/10", border: "border-red-500/10" };
    };

    const colors = getColorClass();

    return (
        <div className="flex flex-col items-center justify-center text-center p-2">
            <div className="relative flex items-center justify-center h-36 w-36">
                {/* SVG Progress Ring */}
                <svg className="w-full h-full transform -rotate-90">
                    <defs>
                        <linearGradient id="emerald-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#10b981" />
                            <stop offset="100%" stopColor="#059669" />
                        </linearGradient>
                        <linearGradient id="blue-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#3b82f6" />
                            <stop offset="100%" stopColor="#2563eb" />
                        </linearGradient>
                        <linearGradient id="amber-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#f59e0b" />
                            <stop offset="100%" stopColor="#d97706" />
                        </linearGradient>
                        <linearGradient id="red-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#ef4444" />
                            <stop offset="100%" stopColor="#dc2626" />
                        </linearGradient>
                    </defs>
                    {/* Background Track Circle */}
                    <circle
                        cx="72"
                        cy="72"
                        r={radius}
                        className="stroke-slate-800"
                        strokeWidth={strokeWidth}
                        fill="transparent"
                    />
                    {/* Glowing outer drop-shadow path */}
                    <circle
                        cx="72"
                        cy="72"
                        r={radius}
                        stroke={colors.stroke}
                        strokeWidth={strokeWidth}
                        fill="transparent"
                        strokeDasharray={circumference}
                        strokeDashoffset={strokeDashoffset}
                        strokeLinecap="round"
                        className="transition-all duration-1000 ease-out opacity-25 blur-[3px]"
                    />
                    {/* Foregound Progress Path */}
                    <circle
                        cx="72"
                        cy="72"
                        r={radius}
                        stroke={colors.stroke}
                        strokeWidth={strokeWidth}
                        fill="transparent"
                        strokeDasharray={circumference}
                        strokeDashoffset={strokeDashoffset}
                        strokeLinecap="round"
                        className="transition-all duration-1000 ease-out"
                    />
                </svg>

                {/* Score Number in Center */}
                <div className="absolute flex flex-col items-center justify-center">
                    <span className="text-4xl font-extrabold text-slate-50 tracking-tight leading-none">
                        {progress}
                    </span>
                    <span className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mt-1.5">
                        MATCH
                    </span>
                </div>
            </div>

            <div className="mt-4">
                <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-bold ${colors.bg} ${colors.text} border border-current/15`}>
                    {level}
                </span>
            </div>
        </div>
    );
}