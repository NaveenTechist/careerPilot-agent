import { FileSearch } from "lucide-react";

type Props = {
    onNewApplication: () => void;
};

export default function EmptyState({ onNewApplication }: Props) {
    return (
        <div className="flex flex-col items-center justify-center py-20 px-6 text-center">
            {/* Illustration */}
            <div className="relative mb-8">
                <div className="flex h-24 w-24 items-center justify-center rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl shadow-slate-950/50">
                    <FileSearch className="w-10 h-10 text-slate-600" />
                </div>
                <div className="absolute -bottom-1 -right-1 flex h-8 w-8 items-center justify-center rounded-xl bg-blue-600 text-white shadow-lg shadow-blue-950/50">
                    <span className="text-lg font-bold leading-none">+</span>
                </div>
            </div>

            <h3 className="text-xl font-bold text-slate-200 tracking-tight">
                No Applications Yet
            </h3>
            <p className="mt-2 text-sm text-slate-500 max-w-xs leading-relaxed">
                Create your first application to start matching your resume with job postings.
            </p>

            <button
                onClick={onNewApplication}
                className="mt-8 inline-flex items-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-500 px-7 py-3 text-sm font-bold text-white shadow-lg shadow-blue-950/40 transition-all duration-200 active:translate-y-0.5 cursor-pointer"
            >
                <span className="text-lg leading-none">+</span>
                New Application
            </button>
        </div>
    );
}
