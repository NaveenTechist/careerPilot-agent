"use client";

export default function DrawerSkeleton() {
    return (
        <div className="space-y-8 animate-pulse">
            {/* Header Area */}
            <div className="space-y-3">
                <div className="h-6 w-3/4 bg-slate-800 rounded-lg skeleton-shimmer" />
                <div className="flex gap-2">
                    <div className="h-4 w-20 bg-slate-800 rounded-full skeleton-shimmer" />
                    <div className="h-4 w-24 bg-slate-800 rounded-full skeleton-shimmer" />
                </div>
            </div>

            {/* Score & Journey Section */}
            <div className="grid grid-cols-3 gap-4 items-center bg-slate-950/20 border border-slate-800/40 rounded-2xl p-5">
                <div className="col-span-1 flex flex-col items-center">
                    <div className="h-16 w-16 bg-slate-800 rounded-full skeleton-shimmer" />
                    <div className="h-3 w-12 bg-slate-800 rounded-lg mt-2 skeleton-shimmer" />
                </div>
                <div className="col-span-2 space-y-2">
                    <div className="h-4 w-full bg-slate-800 rounded-lg skeleton-shimmer" />
                    <div className="h-3 w-5/6 bg-slate-800 rounded-lg skeleton-shimmer" />
                </div>
            </div>

            {/* Journey Timeline Placeholder */}
            <div className="space-y-4 border border-slate-800/40 bg-slate-950/10 rounded-2xl p-5">
                <div className="h-4 w-1/3 bg-slate-800 rounded-lg skeleton-shimmer mb-4" />
                <div className="flex gap-3 items-center">
                    <div className="h-6 w-6 bg-slate-800 rounded-full shrink-0 skeleton-shimmer" />
                    <div className="h-3 w-2/3 bg-slate-800 rounded-lg skeleton-shimmer" />
                </div>
                <div className="flex gap-3 items-center">
                    <div className="h-6 w-6 bg-slate-800 rounded-full shrink-0 skeleton-shimmer" />
                    <div className="h-3 w-1/2 bg-slate-800 rounded-lg skeleton-shimmer" />
                </div>
                <div className="flex gap-3 items-center">
                    <div className="h-6 w-6 bg-slate-800 rounded-full shrink-0 skeleton-shimmer" />
                    <div className="h-3 w-3/5 bg-slate-800 rounded-lg skeleton-shimmer" />
                </div>
            </div>

            {/* Skills & Badges */}
            <div className="space-y-3">
                <div className="h-4 w-1/4 bg-slate-800 rounded-lg skeleton-shimmer" />
                <div className="flex flex-wrap gap-2">
                    <div className="h-7 w-20 bg-slate-800 rounded-full skeleton-shimmer" />
                    <div className="h-7 w-24 bg-slate-800 rounded-full skeleton-shimmer" />
                    <div className="h-7 w-16 bg-slate-800 rounded-full skeleton-shimmer" />
                    <div className="h-7 w-28 bg-slate-800 rounded-full skeleton-shimmer" />
                </div>
            </div>

            {/* Detailed text boxes */}
            <div className="space-y-4">
                <div className="space-y-2">
                    <div className="h-4 w-1/3 bg-slate-800 rounded-lg skeleton-shimmer" />
                    <div className="h-16 w-full bg-slate-900 border border-slate-800 rounded-xl skeleton-shimmer" />
                </div>
                <div className="space-y-2">
                    <div className="h-4 w-1/3 bg-slate-800 rounded-lg skeleton-shimmer" />
                    <div className="h-16 w-full bg-slate-900 border border-slate-800 rounded-xl skeleton-shimmer" />
                </div>
            </div>
        </div>
    );
}
