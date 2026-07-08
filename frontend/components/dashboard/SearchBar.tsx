"use client";

import { Search, SlidersHorizontal, ArrowUpDown } from "lucide-react";

type Filter = "ALL" | "READY" | "CANCELLED" | "PROCEEDED" | "COMPLETED";
type Sort = "newest" | "oldest" | "score_high" | "score_low";

type Props = {
    query: string;
    onQueryChange: (q: string) => void;
    filter: Filter;
    onFilterChange: (f: Filter) => void;
    sort: Sort;
    onSortChange: (s: Sort) => void;
};

const FILTERS: { value: Filter; label: string }[] = [
    { value: "ALL", label: "All" },
    { value: "READY", label: "Pending" },
    { value: "CANCELLED", label: "Cancelled" },
    { value: "PROCEEDED", label: "Proceeded" },
    { value: "COMPLETED", label: "Completed" },
];

const SORTS: { value: Sort; label: string }[] = [
    { value: "newest", label: "Newest" },
    { value: "oldest", label: "Oldest" },
    { value: "score_high", label: "Highest Score" },
    { value: "score_low", label: "Lowest Score" },
];

export default function SearchBar({
    query,
    onQueryChange,
    filter,
    onFilterChange,
    sort,
    onSortChange,
}: Props) {
    return (
        <div className="space-y-4">
            {/* Search Input */}
            <div className="relative group">
                <div className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-blue-400 transition-colors">
                    <Search className="w-4 h-4" />
                </div>
                <input
                    type="text"
                    value={query}
                    onChange={(e) => onQueryChange(e.target.value)}
                    placeholder="Search by company, job title, or status..."
                    className="w-full rounded-xl border border-slate-800 bg-slate-900/40 py-2.5 pl-10 pr-4 text-sm text-slate-100 placeholder-slate-500 outline-none focus:border-blue-500/50 focus:ring-4 focus:ring-blue-500/10 transition-all"
                    aria-label="Search applications"
                />
            </div>

            {/* Filters + Sort row */}
            <div className="flex flex-wrap items-center justify-between gap-3">
                {/* Filters */}
                <div className="flex items-center gap-1.5 flex-wrap">
                    <SlidersHorizontal className="w-3.5 h-3.5 text-slate-500 mr-1 shrink-0" />
                    {FILTERS.map((f) => (
                        <button
                            key={f.value}
                            onClick={() => onFilterChange(f.value)}
                            className={`rounded-lg px-3 py-1.5 text-xs font-medium transition-all cursor-pointer ${
                                filter === f.value
                                    ? "bg-blue-600/10 text-blue-400 border border-blue-500/20"
                                    : "text-slate-500 hover:text-slate-300 hover:bg-slate-900 border border-transparent"
                            }`}
                        >
                            {f.label}
                        </button>
                    ))}
                </div>

                {/* Sort dropdown */}
                <div className="flex items-center gap-1.5">
                    <ArrowUpDown className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                    <select
                        value={sort}
                        onChange={(e) => onSortChange(e.target.value as Sort)}
                        className="rounded-lg border border-slate-800 bg-slate-900/60 px-3 py-1.5 text-xs text-slate-300 outline-none cursor-pointer focus:border-blue-500/50"
                        aria-label="Sort applications"
                    >
                        {SORTS.map((s) => (
                            <option key={s.value} value={s.value}>
                                {s.label}
                            </option>
                        ))}
                    </select>
                </div>
            </div>
        </div>
    );
}
