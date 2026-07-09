"use client";

import { motion } from "framer-motion";
import StatusBadge from "./StatusBadge";
import ScoreBadge from "./ScoreBadge";
import JourneyIndicator from "./JourneyIndicator";
import { Briefcase, Calendar } from "lucide-react";

export type ApplicationSummary = {
    id: string;
    title: string;
    resume_id: string;
    job_id: string;
    match_id: string;
    status: string;
    score: number;
    created_at: string | null;
    updated_at?: string | null;
};

type Props = {
    application: ApplicationSummary;
    onClick: (id: string) => void;
    highlighted?: boolean;
};

export default function ApplicationCard({ application, onClick, highlighted = false }: Props) {
    // Parse "Company • Job Title" format from title
    const parts = application.title?.split(/[•\-–—]/).map((p) => p.trim()) || [];
    const company = parts[0] || "Unknown Company";
    const jobTitle = parts[1] || "Position";

    const formattedDate = application.created_at
        ? new Date(application.created_at).toLocaleDateString("en-US", {
              day: "numeric",
              month: "short",
              year: "numeric",
          })
        : "—";

    return (
        <motion.button
            layout
            onClick={() => onClick(application.id)}
            data-app-id={application.id}
            className={`w-full text-left rounded-2xl border p-5 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:ring-offset-2 focus:ring-offset-slate-950 group cursor-pointer ${
                highlighted
                    ? "card-highlight"
                    : "bg-slate-900/75 border-slate-800/60 hover:border-slate-700 hover:bg-slate-900 hover:shadow-xl hover:shadow-slate-950/40"
            }`}
            aria-label={`View application for ${company} ${jobTitle}`}
        >
            {/* Top row: Company + Status */}
            <div className="flex items-start justify-between gap-3">
                <div className="min-w-0 flex-1">
                    <h3 className="text-sm font-bold text-slate-105 truncate group-hover:text-white transition-colors">
                        {company}
                    </h3>
                    <div className="flex items-center gap-1.5 mt-1">
                        <Briefcase className="w-3 h-3 text-slate-500 shrink-0" />
                        <p className="text-xs text-slate-400 truncate">{jobTitle}</p>
                    </div>
                </div>
                <StatusBadge status={application.status} />
            </div>

            {/* Middle row: Journey Progress Indicator */}
            <div className="mt-4">
                <JourneyIndicator status={application.status} layout="horizontal" />
            </div>

            {/* Bottom row: Date + Score */}
            <div className="flex items-center justify-between mt-4 pt-3.5 border-t border-slate-800/50">
                <div className="flex items-center gap-1.5 text-slate-500">
                    <Calendar className="w-3 h-3" />
                    <span className="text-[11px] font-medium">{formattedDate}</span>
                </div>
                <ScoreBadge score={application.score} />
            </div>
        </motion.button>
    );
}
