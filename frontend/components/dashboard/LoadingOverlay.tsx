"use client";

type Props = {

    text?: string;

};

export default function LoadingOverlay({

    text = "Processing...",

}: Props) {

    return (

        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">

            <div className="rounded-2xl bg-slate-900 p-8">

                <div className="mx-auto h-14 w-14 animate-spin rounded-full border-4 border-slate-700 border-t-blue-500" />

                <p className="mt-5 text-center text-slate-300">

                    {text}

                </p>

            </div>

        </div>

    );

}