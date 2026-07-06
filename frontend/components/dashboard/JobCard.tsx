"use client";

import { useState } from "react";

type Props = {
    session: any;
    onAnalyze: (url: string) => Promise<void>;
};

export default function JobCard({
    session,
    onAnalyze,
}: Props) {

    const [url, setUrl] = useState("");

    const [loading, setLoading] = useState(false);

    async function analyze() {

        if (!url.trim()) return;

        setLoading(true);

        try {

            await onAnalyze(url);

            setUrl("");

        }

        finally {

            setLoading(false);

        }

    }

    return (

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8">

            <div className="flex items-center justify-between">

                <div>

                    <h2 className="text-2xl font-bold text-white">

                        Job Analysis

                    </h2>

                    <p className="mt-1 text-slate-400">

                        Paste a job URL.

                    </p>

                </div>

                {

                    session?.job?.uploaded &&

                    <span className="rounded-full bg-emerald-500/20 px-4 py-2 text-sm text-emerald-400">

                        Ready

                    </span>

                }

            </div>

            {

                session?.job?.uploaded

                    ?

                    <div className="mt-8 space-y-3">

                        <div className="flex justify-between">

                            <span className="text-slate-400">

                                Company

                            </span>

                            <span className="text-white">

                                {session.job.profile.company}

                            </span>

                        </div>

                        <div className="flex justify-between">

                            <span className="text-slate-400">

                                Job Title

                            </span>

                            <span className="text-white">

                                {session.job.profile.title}

                            </span>

                        </div>

                        <div className="flex justify-between">

                            <span className="text-slate-400">

                                Required Skills

                            </span>

                            <span className="text-white">

                                {session.job.profile.required_skills}

                            </span>

                        </div>

                    </div>

                    :

                    <div className="mt-8 space-y-4">

                        <input

                            value={url}

                            onChange={(e) =>
                                setUrl(e.target.value)
                            }

                            placeholder="https://careers.company.com/job"

                            className="w-full rounded-xl border border-slate-700 bg-slate-950 p-4 text-white outline-none focus:border-blue-500"

                        />

                        <button

                            onClick={analyze}

                            disabled={loading}

                            className="rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:opacity-50"

                        >

                            {

                                loading

                                    ?

                                    "Analyzing..."

                                    :

                                    "Analyze Job"

                            }

                        </button>

                    </div>

            }

        </div>

    );

}