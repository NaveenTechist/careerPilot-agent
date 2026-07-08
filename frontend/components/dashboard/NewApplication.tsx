"use client";

import { useState } from "react";
import { api } from "@/services/api";

type Props = {
    onSuccess: () => void;
};

export default function NewApplication({
    onSuccess,
}: Props) {

    const [file, setFile] = useState<File | null>(null);

    const [url, setUrl] = useState("");

    const [loading, setLoading] = useState(false);

    async function submit() {

        if (!file || !url) return;

        setLoading(true);

        try {

            const form = new FormData();

            form.append(
                "resume",
                file,
            );

            form.append(
                "job_url",
                url,
            );

            await api.post(
                "/application",
                form,
                {
                    headers: {
                        "Content-Type":
                            "multipart/form-data",
                    },
                }
            );

            onSuccess();

        } finally {

            setLoading(false);

        }

    }

    return (

        <div className="rounded-2xl bg-slate-900 border border-slate-800 p-8 space-y-6">

            <h2 className="text-2xl font-bold">

                New Application

            </h2>

            <input

                type="file"

                accept=".pdf"

                onChange={(e) =>

                    setFile(
                        e.target.files?.[0] ?? null
                    )

                }

            />

            <input

                value={url}

                onChange={(e) =>

                    setUrl(
                        e.target.value
                    )
                }

                placeholder="Paste Job URL"

                className="w-full rounded-xl bg-slate-950 border border-slate-700 p-3"

            />

            <button

                onClick={submit}

                disabled={loading}

                className="rounded-xl bg-blue-600 px-6 py-3"

            >

                {

                    loading

                        ?

                        "Creating..."

                        :

                        "Create Application"

                }

            </button>

        </div>

    );

}