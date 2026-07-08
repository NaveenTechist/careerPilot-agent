"use client";

import { useRef, useState, useEffect } from "react";
import { 
    FileText, 
    UploadCloud, 
    CheckCircle2, 
    FileCheck, 
    ShieldAlert, 
    ChevronRight,
    Award,
    Briefcase,
    FolderGit,
    FileSpreadsheet
} from "lucide-react";

type Props = {
    session: any;
    onUpload: (file: File) => void;
};

export default function ResumeCard({ session, onUpload }: Props) {
    const inputRef = useRef<HTMLInputElement>(null);
    const [isDragActive, setIsDragActive] = useState(false);
    const [fileName, setFileName] = useState("");
    const [fileSize, setFileSize] = useState("");

    // Listen to custom event from Command Palette
    useEffect(() => {
        const handlePaletteUploadTrigger = () => {
            chooseFile();
        };
        window.addEventListener("trigger-resume-upload", handlePaletteUploadTrigger);
        return () => window.removeEventListener("trigger-resume-upload", handlePaletteUploadTrigger);
    }, []);

    function chooseFile() {
        inputRef.current?.click();
    }

    function handleFile(file: File) {
        if (!file) return;
        if (file.type !== "application/pdf" && !file.name.endsWith(".pdf")) {
            alert("Please upload a PDF file.");
            return;
        }
        
        // Save local stats just for preview
        setFileName(file.name);
        const sizeInMb = (file.size / (1024 * 1024)).toFixed(1);
        setFileSize(`${sizeInMb} MB`);
        
        onUpload(file);
    }

    function onChange(e: React.ChangeEvent<HTMLInputElement>) {
        const file = e.target.files?.[0];
        if (file) handleFile(file);
    }

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setIsDragActive(true);
        } else if (e.type === "dragleave") {
            setIsDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const isUploaded = !!session?.resume?.uploaded;
    const profile = session?.resume?.profile;

    return (
        <div className="premium-card p-6 md:p-8 flex flex-col justify-between min-h-[380px] transition-all duration-300">
            {/* Header info */}
            <div>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2.5">
                        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/10 text-blue-400">
                            <FileText className="w-5 h-5" />
                        </div>
                        <div>
                            <h2 className="text-lg font-bold text-white tracking-tight">
                                Resume
                            </h2>
                            <p className="text-xs text-slate-400 mt-0.5">
                                Upload your latest resume to parse skills
                            </p>
                        </div>
                    </div>

                    {isUploaded && (
                        <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-400 border border-emerald-500/20">
                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                            Uploaded
                        </span>
                    )}
                </div>

                {/* Drag and Drop Upload Area */}
                {!isUploaded ? (
                    <div
                        onDragEnter={handleDrag}
                        onDragOver={handleDrag}
                        onDragLeave={handleDrag}
                        onDrop={handleDrop}
                        onClick={chooseFile}
                        className={`mt-6 flex flex-col items-center justify-center rounded-2xl border border-dashed p-8 text-center cursor-pointer transition-all duration-200 group ${
                            isDragActive
                                ? "border-blue-500 bg-blue-600/5 shadow-[0_0_15px_rgba(59,130,246,0.1)]"
                                : "border-slate-800 bg-slate-900/30 hover:border-slate-700 hover:bg-slate-900/50"
                        }`}
                    >
                        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-900 border border-slate-800 text-slate-400 group-hover:text-blue-400 group-hover:border-slate-700 group-hover:scale-105 transition-all duration-200">
                            <UploadCloud className="w-6 h-6" />
                        </div>
                        <p className="mt-4 text-sm font-semibold text-slate-200">
                            Drag & drop your file here, or{" "}
                            <span className="text-blue-500 hover:underline">browse</span>
                        </p>
                        <p className="mt-1.5 text-xs text-slate-500">
                            PDF format only (Max 5MB)
                        </p>
                    </div>
                ) : (
                    /* Display Parsed Info */
                    <div className="mt-6 space-y-6">
                        {/* File Details Bar */}
                        <div className="flex items-center justify-between p-4 rounded-xl bg-slate-900/60 border border-slate-850">
                            <div className="flex items-center gap-3 min-w-0">
                                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-red-500/10 text-red-400">
                                    <FileSpreadsheet className="w-5 h-5" />
                                </div>
                                <div className="min-w-0">
                                    <h4 className="text-sm font-bold text-slate-200 truncate pr-2">
                                        {profile?.name || fileName || "Resume.pdf"}
                                    </h4>
                                    <p className="text-xs text-slate-500 mt-0.5">
                                        {fileSize || "1.8 MB"} • Parsed Successfully
                                    </p>
                                </div>
                            </div>
                            <div className="flex items-center gap-1 bg-emerald-500/15 text-emerald-400 px-2 py-0.5 rounded text-[11px] font-semibold border border-emerald-500/10">
                                <CheckCircle2 className="w-3.5 h-3.5" />
                                Ready
                            </div>
                        </div>

                        {/* Metadata Stats Grid */}
                        <div className="grid grid-cols-2 gap-4">
                            {/* Skills Card */}
                            <div className="p-3.5 rounded-xl bg-slate-900/40 border border-slate-850/60 hover:border-slate-800 transition-all duration-200">
                                <div className="flex items-center gap-2 text-slate-400">
                                    <Award className="w-4 h-4 text-blue-400" />
                                    <span className="text-xs font-semibold tracking-wide uppercase">Skills Found</span>
                                </div>
                                <div className="mt-2 flex items-baseline gap-1.5">
                                    <span className="text-2xl font-bold text-slate-100">{profile?.skills ?? 0}</span>
                                    <span className="text-[11px] text-slate-500">skills</span>
                                </div>
                            </div>

                            {/* Experience Card */}
                            <div className="p-3.5 rounded-xl bg-slate-900/40 border border-slate-850/60 hover:border-slate-800 transition-all duration-200">
                                <div className="flex items-center gap-2 text-slate-400">
                                    <Briefcase className="w-4 h-4 text-indigo-400" />
                                    <span className="text-xs font-semibold tracking-wide uppercase">Experience</span>
                                </div>
                                <div className="mt-2 flex items-baseline gap-1.5">
                                    <span className="text-2xl font-bold text-slate-100">{profile?.experience ?? 0}</span>
                                    <span className="text-[11px] text-slate-500">{profile?.experience === 1 ? "role" : "roles"}</span>
                                </div>
                            </div>

                            {/* Projects Card */}
                            <div className="p-3.5 rounded-xl bg-slate-900/40 border border-slate-850/60 hover:border-slate-800 transition-all duration-200 col-span-2">
                                <div className="flex items-center gap-2 text-slate-400">
                                    <FolderGit className="w-4 h-4 text-cyan-400" />
                                    <span className="text-xs font-semibold tracking-wide uppercase">Projects Listed</span>
                                </div>
                                <div className="mt-2 flex items-baseline gap-1.5">
                                    <span className="text-2xl font-bold text-slate-100">{profile?.projects ?? 0}</span>
                                    <span className="text-[11px] text-slate-500">projects indexed</span>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Hidden Input field */}
            <input
                ref={inputRef}
                type="file"
                hidden
                accept=".pdf"
                onChange={onChange}
            />

            {/* Action buttons footer */}
            <div className="mt-6 pt-4 border-t border-slate-900 flex justify-end">
                {isUploaded ? (
                    <button
                        onClick={chooseFile}
                        className="inline-flex items-center gap-1.5 rounded-xl border border-slate-800 hover:border-slate-700 bg-slate-900/50 hover:bg-slate-900 px-4 py-2 text-xs font-semibold text-slate-300 hover:text-white transition-all duration-150"
                    >
                        Re-upload PDF
                    </button>
                ) : (
                    <button
                        onClick={chooseFile}
                        className="inline-flex items-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-500 px-5 py-2.5 text-xs font-bold text-white shadow-md shadow-blue-900/30 transition-all duration-150 hover:-translate-y-0.5 active:translate-y-0"
                    >
                        Browse Files
                    </button>
                )}
            </div>
        </div>
    );
}