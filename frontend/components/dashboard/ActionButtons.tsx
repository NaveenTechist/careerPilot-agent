"use client";

import { useState } from "react";
import { Play, X, Loader2 } from "lucide-react";

type Props = {
    matchId: string;
    shouldApply: boolean;
    onProceed: () => void | Promise<void>;
    onCancel: () => void | Promise<void>;
};

export default function ActionButtons({
    onProceed,
    onCancel,
    matchId,
    shouldApply,
}: Props) {
    const [isProceeding, setIsProceeding] = useState(false);
    const [isCancelling, setIsCancelling] = useState(false);

    async function handleProceedClick() {
        setIsProceeding(true);
        try {
            await onProceed();
        } catch (err) {
            console.error("Failed to proceed:", err);
        } finally {
            setIsProceeding(false);
        }
    }

    async function handleCancelClick() {
        setIsCancelling(true);
        try {
            await onCancel();
        } catch (err) {
            console.error("Failed to cancel:", err);
        } finally {
            setIsCancelling(false);
        }
    }

    return (
        <div className="mt-8 pt-6 border-t border-slate-900/60 flex flex-col sm:flex-row justify-end gap-4">
            <button
                onClick={handleCancelClick}
                disabled={isCancelling || isProceeding}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-xl border border-red-500/30 bg-transparent px-6 py-3 font-semibold text-red-400 hover:bg-red-500/10 active:bg-red-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-150 cursor-pointer text-sm"
            >
                {isCancelling ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                    <X className="w-4 h-4" />
                )}
                Cancel Application
            </button>

            <button
                onClick={handleProceedClick}
                disabled={!shouldApply || isProceeding || isCancelling}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-3 font-semibold text-white shadow-lg shadow-blue-900/30 hover:from-blue-500 hover:to-indigo-500 hover:shadow-blue-800/40 active:translate-y-0.5 disabled:translate-y-0 disabled:from-slate-800 disabled:to-slate-800 disabled:text-slate-500 disabled:shadow-none disabled:cursor-not-allowed transition-all duration-150 cursor-pointer text-sm"
            >
                {isProceeding ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                    <Play className="w-4 h-4 fill-current text-white" />
                )}
                Proceed Automation
            </button>
        </div>
    );
}