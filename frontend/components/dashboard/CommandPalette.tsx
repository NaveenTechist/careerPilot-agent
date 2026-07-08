"use client";

import { useEffect, useState, useRef } from "react";
import {
    Search,
    FileText,
    Link as LinkIcon,
    Sparkles,
    Play,
    Compass,
    Settings,
    Keyboard,
    X,
    ArrowRight
} from "lucide-react";

interface CommandItem {
    id: string;
    title: string;
    subtitle: string;
    shortcut?: string;
    icon: React.ReactNode;
    category: "Actions" | "Navigation" | "Resume & Jobs";
    action: () => void;
}

interface Props {
    open: boolean;
    onClose: () => void;
}

export default function CommandPalette({ open, onClose }: Props) {
    const [search, setSearch] = useState("");
    const [activeIndex, setActiveIndex] = useState(0);
    const inputRef = useRef<HTMLInputElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);

    // List of all items
    const getItems = (): CommandItem[] => [
        {
            id: "upload-resume",
            title: "Upload Resume",
            subtitle: "Drag and drop or select a PDF resume file",
            shortcut: "U",
            icon: <FileText className="w-5 h-5 text-blue-400" />,
            category: "Actions",
            action: () => {
                window.dispatchEvent(new CustomEvent("trigger-resume-upload"));
                onClose();
            }
        },
        {
            id: "focus-job",
            title: "Analyze Job URL",
            subtitle: "Paste a job posting link to extract requirements",
            shortcut: "J",
            icon: <LinkIcon className="w-5 h-5 text-purple-400" />,
            category: "Actions",
            action: () => {
                window.dispatchEvent(new CustomEvent("focus-job-input"));
                onClose();
            }
        },
        {
            id: "analyze-match",
            title: "Analyze Resume Match",
            subtitle: "Compare current resume with analyzed job",
            shortcut: "M",
            icon: <Sparkles className="w-5 h-5 text-emerald-400" />,
            category: "Actions",
            action: () => {
                window.dispatchEvent(new CustomEvent("trigger-match-analysis"));
                onClose();
            }
        },
        {
            id: "scroll-match",
            title: "Open Match Result",
            subtitle: "View the AI matching details and recommendations",
            shortcut: "R",
            icon: <Play className="w-5 h-5 text-amber-400" />,
            category: "Actions",
            action: () => {
                window.dispatchEvent(new CustomEvent("scroll-to-match"));
                onClose();
            }
        },
        {
            id: "nav-dashboard",
            title: "Go to Dashboard",
            subtitle: "Main control panel and active workflow",
            shortcut: "G + D",
            icon: <Compass className="w-5 h-5 text-slate-400" />,
            category: "Navigation",
            action: () => {
                window.scrollTo({ top: 0, behavior: "smooth" });
                onClose();
            }
        },
        {
            id: "nav-settings",
            title: "Go to Settings",
            subtitle: "Configure credentials and automation rules",
            shortcut: "G + S",
            icon: <Settings className="w-5 h-5 text-slate-400" />,
            category: "Navigation",
            action: () => {
                window.dispatchEvent(new CustomEvent("show-settings-alert"));
                onClose();
            }
        }
    ];

    const filteredItems = getItems().filter((item) =>
        item.title.toLowerCase().includes(search.toLowerCase()) ||
        item.subtitle.toLowerCase().includes(search.toLowerCase()) ||
        item.category.toLowerCase().includes(search.toLowerCase())
    );

    // Auto-focus input on open
    useEffect(() => {
        if (open) {
            setSearch("");
            setActiveIndex(0);
            setTimeout(() => inputRef.current?.focus(), 50);
        }
    }, [open]);

    // Handle keydown events inside the modal
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (!open) return;

            if (e.key === "Escape") {
                e.preventDefault();
                onClose();
            } else if (e.key === "ArrowDown") {
                e.preventDefault();
                setActiveIndex((prev) => (prev + 1) % filteredItems.length);
            } else if (e.key === "ArrowUp") {
                e.preventDefault();
                setActiveIndex((prev) => (prev - 1 + filteredItems.length) % filteredItems.length);
            } else if (e.key === "Enter") {
                e.preventDefault();
                if (filteredItems[activeIndex]) {
                    filteredItems[activeIndex].action();
                }
            }
        };

        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, [open, activeIndex, filteredItems, onClose]);

    // Click outside to close
    const handleBackdropClick = (e: React.MouseEvent) => {
        if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
            onClose();
        }
    };

    if (!open) return null;

    // Group filtered items by category
    const categories = Array.from(new Set(filteredItems.map((item) => item.category)));

    // Flatten array items index mapping
    let flatIndex = 0;

    return (
        <div
            onClick={handleBackdropClick}
            className="fixed inset-0 z-[100] flex items-start justify-center bg-slate-950/80 p-4 pt-[12vh] backdrop-blur-md transition-opacity duration-200"
        >
            <div
                ref={containerRef}
                className="w-full max-w-xl overflow-hidden rounded-2xl border border-slate-800 bg-[#0b0f19] shadow-2xl shadow-black/80 animate-in fade-in zoom-in-95 duration-150"
            >
                {/* Search Input Area */}
                <div className="relative flex items-center border-b border-slate-850 px-4 py-3.5">
                    <Search className="mr-3 h-5 w-5 text-slate-400 shrink-0" />
                    <input
                        ref={inputRef}
                        type="text"
                        placeholder="Search command palette..."
                        value={search}
                        onChange={(e) => {
                            setSearch(e.target.value);
                            setActiveIndex(0);
                        }}
                        className="w-full bg-transparent text-slate-100 placeholder-slate-500 outline-none text-base font-sans"
                    />
                    <button
                        onClick={onClose}
                        className="ml-2 rounded-lg p-1 text-slate-500 hover:bg-slate-900 hover:text-slate-300 transition-colors"
                    >
                        <X className="h-4 w-4" />
                    </button>
                </div>

                {/* Commands List Area */}
                <div className="max-h-[360px] overflow-y-auto p-2 custom-scrollbar">
                    {filteredItems.length === 0 ? (
                        <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
                            <Keyboard className="h-8 w-8 text-slate-600 mb-2" />
                            <p className="text-slate-400 font-medium">No results found for &ldquo;{search}&rdquo;</p>
                            <p className="text-slate-500 text-xs mt-1">Try searching for other commands or navigation</p>
                        </div>
                    ) : (
                        categories.map((category) => {
                            const categoryItems = filteredItems.filter(item => item.category === category);
                            return (
                                <div key={category} className="mb-2">
                                    <div className="px-3 py-1.5 text-xs font-semibold uppercase tracking-wider text-slate-500">
                                        {category}
                                    </div>
                                    <div className="space-y-0.5">
                                        {categoryItems.map((item) => {
                                            const currentFlatIndex = flatIndex++;
                                            const isSelected = currentFlatIndex === activeIndex;
                                            return (
                                                <button
                                                    key={item.id}
                                                    onClick={item.action}
                                                    onMouseEnter={() => setActiveIndex(currentFlatIndex)}
                                                    className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-left transition-all duration-150 ${
                                                        isSelected
                                                            ? "bg-slate-900/90 text-white"
                                                            : "bg-transparent text-slate-300"
                                                    }`}
                                                >
                                                    <div className="flex items-center gap-3 min-w-0">
                                                        <div className={`p-1.5 rounded-lg shrink-0 ${
                                                            isSelected ? "bg-slate-800 text-white" : "bg-slate-950/80"
                                                        }`}>
                                                            {item.icon}
                                                        </div>
                                                        <div className="min-w-0">
                                                            <div className="font-medium text-sm text-slate-100 leading-snug">
                                                                {item.title}
                                                            </div>
                                                            <div className="text-xs text-slate-400 truncate mt-0.5">
                                                                {item.subtitle}
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div className="flex items-center gap-2 shrink-0">
                                                        {item.shortcut && (
                                                            <kbd className={`hidden sm:inline-flex h-5 items-center rounded border border-slate-700 bg-slate-950 px-1.5 font-mono text-[10px] font-medium text-slate-400 ${
                                                                isSelected ? "border-slate-600 text-slate-200" : ""
                                                            }`}>
                                                                {item.shortcut}
                                                            </kbd>
                                                        )}
                                                        {isSelected && (
                                                            <ArrowRight className="h-4 w-4 text-blue-500 animate-pulse shrink-0" />
                                                        )}
                                                    </div>
                                                </button>
                                            );
                                        })}
                                    </div>
                                </div>
                            );
                        })
                    )}
                </div>

                {/* Footer hints */}
                <div className="flex items-center justify-between border-t border-slate-850 px-4 py-2 text-[11px] text-slate-500 bg-slate-950/50">
                    <div className="flex items-center gap-3">
                        <span className="flex items-center gap-1"><kbd className="rounded bg-slate-900 px-1 py-0.5 border border-slate-800">↑↓</kbd> Navigate</span>
                        <span className="flex items-center gap-1"><kbd className="rounded bg-slate-900 px-1 py-0.5 border border-slate-800">Enter</kbd> Select</span>
                        <span className="flex items-center gap-1"><kbd className="rounded bg-slate-900 px-1 py-0.5 border border-slate-800">ESC</kbd> Close</span>
                    </div>
                    <div className="hidden sm:block font-mono text-slate-600">
                        CareerPilot AI
                    </div>
                </div>
            </div>
        </div>
    );
}
