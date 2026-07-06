"use client";

type Props = {

    open: boolean;

    score: number;

    onConfirm: () => void;

    onClose: () => void;

};

export default function ConfirmModal({

    open,

    score,

    onConfirm,

    onClose,

}: Props) {

    if (!open) return null;

    return (

        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">

            <div className="w-[480px] rounded-2xl bg-slate-900 p-8 shadow-2xl">

                <h2 className="text-2xl font-bold text-white">

                    AI Recommendation

                </h2>

                <p className="mt-5 text-slate-300">

                    Match Score

                    <span className="ml-2 font-bold text-blue-400">

                        {score}%

                    </span>

                </p>

                <p className="mt-5 leading-7 text-slate-400">

                    AI recommends not applying.

                    Do you still want to continue?

                </p>

                <div className="mt-8 flex justify-end gap-4">

                    <button

                        onClick={onClose}

                        className="rounded-lg border border-slate-700 px-5 py-2 text-white"

                    >

                        Go Back

                    </button>

                    <button

                        onClick={onConfirm}

                        className="rounded-lg bg-blue-600 px-5 py-2 text-white"

                    >

                        Continue Anyway

                    </button>

                </div>

            </div>

        </div>

    );

}