"use client";

import { useState } from "react";
import { api } from "@/services/api";

export default function JobUrlForm() {
    const [url, setUrl] = useState("");

    async function analyzeJob() {
        const response = await api.post("/job/", {
            url,
        });

        console.log(response.data);
    }

    return (
        <div className="space-y-3">

            <input
                type="text"
                placeholder="Paste Job URL..."
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="w-full rounded border p-2"
            />

            <button
                onClick={analyzeJob}
                className="rounded bg-green-600 px-4 py-2 text-white"
            >
                Analyze Job
            </button>

        </div>
    );
}