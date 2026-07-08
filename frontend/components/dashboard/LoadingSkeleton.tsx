export default function LoadingSkeleton() {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: 6 }).map((_, i) => (
                <div
                    key={i}
                    className="rounded-2xl bg-slate-900/60 border border-slate-800/50 p-5 animate-pulse"
                >
                    <div className="flex items-center justify-between mb-4">
                        <div className="h-4 w-28 rounded-lg bg-slate-800" />
                        <div className="h-5 w-14 rounded-full bg-slate-800" />
                    </div>
                    <div className="h-3.5 w-36 rounded-lg bg-slate-800/60 mb-3" />
                    <div className="flex items-center justify-between mt-5">
                        <div className="h-3 w-20 rounded-lg bg-slate-800/40" />
                        <div className="h-6 w-12 rounded-full bg-slate-800" />
                    </div>
                </div>
            ))}
        </div>
    );
}
