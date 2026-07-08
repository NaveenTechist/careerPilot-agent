"use client";

import { useState, useRef } from "react";
import { X, Upload, FileText, AlertCircle, Loader2 } from "lucide-react";
import { createApplication } from "@/services/application";

type Props = {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
};

export default function NewApplicationModal({ isOpen, onClose, onSuccess }: Props) {
    const [file, setFile] = useState<File | null>(null);
    const [url, setUrl] = useState("");
    const [dragActive, setDragActive] = useState(false);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const fileInputRef = useRef<HTMLInputElement>(null);

    if (!isOpen) return null;

    // Validate URL client-side
    const validateJobUrl = (inputUrl: string): string | null => {
        const trimmed = inputUrl.trim();
        if (!trimmed) return "Please enter a valid job posting URL.";
        if (!trimmed.startsWith("http://") && !trimmed.startsWith("https://")) {
            return "Please enter a valid job posting URL.";
        }
        try {
            const parsed = new URL(trimmed);
            const host = parsed.hostname.toLowerCase();
            const path = parsed.pathname.toLowerCase();

            // Reject simple names / keywords / search index roots
            const invalidKeywords = ["google", "facebook", "abcd", "123", "test", "example", "linkedin", "careers"];
            if (invalidKeywords.some(kw => host.includes(kw) && (path === "/" || path === ""))) {
                return "Please enter a valid job posting URL.";
            }
            if (host === "www.google.com" || host === "google.com" || host === "example.com") {
                return "Please enter a valid job posting URL.";
            }

            return null;
        } catch {
            return "Please enter a valid job posting URL.";
        }
    };

    // File check helper
    const handleFile = (selectedFile: File) => {
        setErrorMsg(null);

        // Only allow PDF
        if (selectedFile.type !== "application/pdf" && !selectedFile.name.endsWith(".pdf")) {
            setErrorMsg("Only PDF resumes are supported.");
            setFile(null);
            return;
        }

        // Limit size to 10MB
        if (selectedFile.size > 10 * 1024 * 1024) {
            setErrorMsg("Resume size exceeds 10MB.");
            setFile(null);
            return;
        }

        setFile(selectedFile);
    };

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const submit = async () => {
        setErrorMsg(null);

        if (!file) {
            setErrorMsg("Please upload a resume PDF.");
            return;
        }

        const urlValidationError = validateJobUrl(url);
        if (urlValidationError) {
            setErrorMsg(urlValidationError);
            return;
        }

        setLoading(true);
        try {
            await createApplication(file, url.trim());
            onSuccess();
        } catch (err: any) {
            setErrorMsg(err.message || "Failed to create application.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm transition-all duration-300">
            {/* Modal Container */}
            <div 
                className="w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden transition-all duration-300 transform scale-100 flex flex-col max-h-[90vh]"
                onClick={(e) => e.stopPropagation()}
            >
                {/* Header */}
                <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800/80">
                    <h3 className="text-lg font-bold text-white tracking-tight">
                        New Application
                    </h3>
                    <button
                        onClick={onClose}
                        disabled={loading}
                        className="rounded-lg p-1.5 text-slate-450 hover:bg-slate-800 hover:text-white transition-colors cursor-pointer disabled:opacity-55"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Form fields */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6">
                    
                    {/* Error Banner */}
                    {errorMsg && (
                        <div className="p-3.5 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs flex gap-2.5 items-start">
                            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                            <p className="leading-relaxed">{errorMsg}</p>
                        </div>
                    )}

                    {/* Resume Upload Drag & Drop Area */}
                    <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                            Upload Resume (PDF only)
                        </label>
                        <div
                            onDragEnter={handleDrag}
                            onDragOver={handleDrag}
                            onDragLeave={handleDrag}
                            onDrop={handleDrop}
                            onClick={() => !loading && fileInputRef.current?.click()}
                            className={`relative rounded-xl border-2 border-dashed p-6 text-center cursor-pointer transition-all duration-200 flex flex-col items-center justify-center min-h-[140px] ${
                                dragActive 
                                    ? "border-blue-500 bg-blue-500/5" 
                                    : file 
                                        ? "border-emerald-500/40 bg-emerald-500/5" 
                                        : "border-slate-800 hover:border-slate-700 bg-slate-950/20"
                            } ${loading ? "opacity-50 pointer-events-none" : ""}`}
                        >
                            <input
                                ref={fileInputRef}
                                type="file"
                                accept=".pdf"
                                onChange={handleFileInput}
                                className="hidden"
                                disabled={loading}
                            />
                            {file ? (
                                <>
                                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400">
                                        <FileText className="w-6 h-6" />
                                    </div>
                                    <h4 className="mt-3 text-sm font-semibold text-slate-200 truncate max-w-[280px]">
                                        {file.name}
                                    </h4>
                                    <p className="mt-1 text-[11px] text-slate-500">
                                        {(file.size / (1024 * 1024)).toFixed(2)} MB • Click to replace
                                    </p>
                                </>
                            ) : (
                                <>
                                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-900 text-slate-400">
                                        <Upload className="w-5 h-5" />
                                    </div>
                                    <h4 className="mt-3 text-sm font-semibold text-slate-350">
                                        Drag & drop resume here
                                    </h4>
                                    <p className="mt-1 text-xs text-slate-500">
                                        or click to browse from files (Max 10MB)
                                    </p>
                                </>
                            )}
                        </div>
                    </div>

                    {/* Job URL Input */}
                    <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                            Job Posting URL
                        </label>
                        <input
                            type="text"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            placeholder="https://linkedin.com/jobs/view/..."
                            disabled={loading}
                            className="w-full rounded-xl border border-slate-800 bg-slate-950/40 p-3.5 text-sm text-slate-100 placeholder-slate-550 outline-none transition-all duration-200 focus:border-blue-500/70 focus:bg-slate-950/70 focus:ring-4 focus:ring-blue-500/10 disabled:opacity-50"
                        />
                    </div>
                </div>

                {/* Footer Buttons */}
                <div className="px-6 py-4 border-t border-slate-800/80 bg-slate-950/30 flex justify-end gap-3.5">
                    <button
                        onClick={onClose}
                        disabled={loading}
                        className="rounded-xl border border-slate-800 hover:border-slate-700 bg-transparent px-5 py-2.5 text-xs font-bold text-slate-300 hover:text-white transition-all duration-150 cursor-pointer disabled:opacity-50"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={submit}
                        disabled={loading || !file || !url.trim()}
                        className="inline-flex items-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 disabled:text-slate-500 px-6 py-2.5 text-xs font-bold text-white transition-all duration-150 active:translate-y-0.5 disabled:translate-y-0 cursor-pointer"
                    >
                        {loading ? (
                            <>
                                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                                Creating Application...
                            </>
                        ) : (
                            "Create Application"
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
