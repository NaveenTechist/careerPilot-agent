"use client";

import { useRef } from "react";

type Props = {

    session: any;

    onUpload: (

        file: File

    ) => void;

};

export default function ResumeCard({

    session,

    onUpload,

}: Props) {

    const inputRef =

        useRef<HTMLInputElement>(null);

    function chooseFile() {

        inputRef.current?.click();

    }

    function onChange(

        e: React.ChangeEvent<HTMLInputElement>

    ) {

        const file =

            e.target.files?.[0];

        if (!file) return;

        onUpload(file);

    }

    return (

        <div

            className="rounded-2xl border border-slate-800 bg-slate-900 p-8"

        >

            <div className="flex items-center justify-between">

                <div>

                    <h2 className="text-2xl font-bold text-white">

                        Resume

                    </h2>

                    <p className="mt-1 text-slate-400">

                        Upload your latest resume.

                    </p>

                </div>

                {

                    session?.resume?.uploaded && (

                        <span className="rounded-full bg-emerald-500/20 px-4 py-2 text-sm text-emerald-400">

                            Uploaded

                        </span>

                    )

                }

            </div>

            {

                session?.resume?.uploaded

                    ?

                    (

                        <div className="mt-8 space-y-3">

                            <div className="flex justify-between">

                                <span className="text-slate-400">

                                    Name

                                </span>

                                <span className="font-medium text-white">

                                    {session.resume.profile.name}

                                </span>

                            </div>

                            <div className="flex justify-between">

                                <span className="text-slate-400">

                                    Skills

                                </span>

                                <span className="text-white">

                                    {session.resume.profile.skills}

                                </span>

                            </div>

                            <div className="flex justify-between">

                                <span className="text-slate-400">

                                    Projects

                                </span>

                                <span className="text-white">

                                    {session.resume.profile.projects}

                                </span>

                            </div>

                            <div className="flex justify-between">

                                <span className="text-slate-400">

                                    Experience

                                </span>

                                <span className="text-white">

                                    {session.resume.profile.experience}

                                </span>

                            </div>

                        </div>

                    )

                    :

                    (

                        <div className="mt-8">

                            <button

                                onClick={chooseFile}

                                className="rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-700"

                            >

                                Upload Resume

                            </button>

                        </div>

                    )

            }

            <input

                ref={inputRef}

                type="file"

                hidden

                accept=".pdf"

                onChange={onChange}

            />

        </div>

    );

}