"use client";

type Props = {

    open: boolean;

    message: string;

};

export default function Notification({

    open,

    message,

}: Props) {

    if (!open) return null;

    return (

        <div

            className="fixed right-6 top-6 z-50 rounded-xl bg-slate-900 px-6 py-4 shadow-2xl border border-blue-500"

        >

            <div className="flex items-center gap-3">

                <div className="h-3 w-3 rounded-full bg-blue-500 animate-pulse" />

                <p className="text-white">

                    {message}

                </p>

            </div>

        </div>

    );

}