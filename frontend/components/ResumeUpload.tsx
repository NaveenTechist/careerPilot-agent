"use client";

import { useState } from "react";
import { api } from "@/services/api";

export default function ResumeUpload() {
    const [file, setFile] = useState<File | null>(null);

    async function uploadResume() {
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        const response = await api.post(
            "/resume",
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            }
        );

        console.log(response.data);
    }

    return (
        <div className="space-y-3">

            <input
                type="file"
                accept=".pdf"
                onChange={(e) =>
                    setFile(e.target.files?.[0] ?? null)
                }
            />

            <button
                onClick={uploadResume}
                className="rounded bg-blue-600 px-4 py-2 text-white"
            >
                Upload Resume
            </button>

        </div>
    );
}