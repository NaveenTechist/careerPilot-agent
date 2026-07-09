export default function LoadingSkeleton() {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: 6 }).map((_, i) => (
                <div
                    key={i}
                    className="rounded-2xl bg-slate-900/60 border border-slate-800/50 p-5"
                    style={{ animationDelay: `${i * 80}ms` }}
                >
                    {/* Top row: Company + Status */}
                    <div className="flex items-center justify-between mb-3">
                        <div className="space-y-2 flex-1">
                            <div className="h-4 w-32 rounded-lg skeleton-shimmer" />
                            <div className="h-3 w-24 rounded-lg skeleton-shimmer" />
                        </div>
                        <div className="h-5 w-16 rounded-full skeleton-shimmer" />
                    </div>

                    {/* Journey indicator placeholder */}
                    <div className="flex items-center justify-between gap-2 my-4 px-1">
                        {Array.from({ length: 6 }).map((_, j) => (
                            <div key={j} className="flex flex-col items-center gap-1.5">
                                <div className="h-5 w-5 rounded-full skeleton-shimmer" />
                                <div className="h-2 w-8 rounded skeleton-shimmer" />
                            </div>
                        ))}
                    </div>

                    {/* Bottom row: Date + Score */}
                    <div className="flex items-center justify-between mt-4 pt-3.5 border-t border-slate-800/50">
                        <div className="h-3 w-20 rounded-lg skeleton-shimmer" />
                        <div className="h-6 w-12 rounded-full skeleton-shimmer" />
                    </div>
                </div>
            ))}
        </div>
    );
}
