"use client";

import { useEffect, useState } from "react";
import { Bell, BriefcaseBusiness, Search, Sparkles } from "lucide-react";
import CommandPalette from "./CommandPalette";

export default function Header() {
    const [isPaletteOpen, setIsPaletteOpen] = useState(false);
    const [isScrolled, setIsScrolled] = useState(false);
    const [notificationsCount, setNotificationsCount] = useState(3);

    // Toggle command palette on Ctrl+K or Cmd+K
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
                e.preventDefault();
                setIsPaletteOpen((prev) => !prev);
            }
        };
        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, []);

    // Change background style on scroll
    useEffect(() => {
        const handleScroll = () => {
            if (window.scrollY > 10) {
                setIsScrolled(true);
            } else {
                setIsScrolled(false);
            }
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    return (
        <>
            <header
                className={`sticky top-0 z-[40] w-full transition-all duration-300 ${
                    isScrolled
                        ? "glass-header bg-[#020617]/85 border-slate-800/80 shadow-lg shadow-black/35 py-3"
                        : "bg-transparent border-b border-transparent py-5"
                }`}
            >
                <div className="mx-auto flex max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
                    {/* Left: Brand logo & titles */}
                    <div className="flex items-center gap-3.5 group cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}>
                        <div className="relative flex h-11 w-11 items-center justify-center rounded-[14px] bg-gradient-to-br from-blue-600 via-indigo-500 to-cyan-500 shadow-md shadow-blue-900/35 transition-transform duration-300 group-hover:scale-105">
                            <BriefcaseBusiness size={20} className="text-white" />
                            <div className="absolute inset-0 rounded-[14px] bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                        </div>
                        <div>
                            <div className="flex items-center gap-1.5">
                                <h1 className="text-lg font-bold tracking-tight text-white sm:text-xl leading-none">
                                    CareerPilot AI
                                </h1>
                                <Sparkles size={13} className="text-blue-400 animate-pulse" />
                            </div>
                            <p className="hidden text-xs text-slate-400 sm:block mt-1 font-medium tracking-wide">
                                AI Career Copilot
                            </p>
                        </div>
                    </div>

                    {/* Middle: Modern Glass Search Bar trigger */}
                    <div className="relative hidden md:block max-w-md w-full mx-8">
                        <button
                            onClick={() => setIsPaletteOpen(true)}
                            className="w-full flex items-center justify-between rounded-xl border border-slate-800/80 bg-slate-900/40 hover:bg-slate-900/70 hover:border-slate-700/80 px-4 py-2.5 text-left text-sm text-slate-400 hover:text-slate-300 transition-all duration-150 cursor-pointer shadow-inner focus:outline-none"
                        >
                            <div className="flex items-center gap-2.5">
                                <Search size={16} className="text-slate-500" />
                                <span className="font-sans">Search anything...</span>
                            </div>
                            <div className="flex items-center gap-1.5">
                                <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-0.5 rounded border border-slate-700 bg-slate-950 px-1.5 font-mono text-[10px] font-medium text-slate-400">
                                    <span>⌘</span>K
                                </kbd>
                            </div>
                        </button>
                    </div>

                    {/* Right: Actions */}
                    <div className="flex items-center gap-3">
                        {/* Mobile Search Button */}
                        <button
                            onClick={() => setIsPaletteOpen(true)}
                            className="md:hidden flex h-10 w-10 items-center justify-center rounded-xl border border-slate-800 bg-slate-900/60 text-slate-400 hover:border-slate-700 hover:text-white transition-all duration-150"
                        >
                            <Search size={18} />
                        </button>

                        {/* Notification Button */}
                        <div className="relative">
                            <button
                                onClick={() => setNotificationsCount(0)}
                                className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-slate-800 bg-slate-900/60 text-slate-400 hover:border-slate-700 hover:text-white transition-all duration-150 hover:bg-slate-800/50"
                            >
                                <Bell size={18} />
                                {notificationsCount > 0 && (
                                    <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-blue-600 text-[9px] font-bold text-white shadow-sm ring-2 ring-slate-950 animate-bounce">
                                        {notificationsCount}
                                    </span>
                                )}
                            </button>
                        </div>

                        {/* Profile Avatar with online status */}
                        <div className="relative group cursor-pointer">
                            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 via-indigo-600 to-cyan-500 font-bold text-white shadow-md shadow-blue-950/40 transition-transform duration-200 hover:scale-105">
                                N
                            </div>
                            <span className="absolute bottom-0 right-0 h-3 w-3 rounded-full border-2 border-slate-950 bg-emerald-500" />
                        </div>
                    </div>
                </div>
            </header>

            {/* Command Palette Modal */}
            <CommandPalette
                open={isPaletteOpen}
                onClose={() => setIsPaletteOpen(false)}
            />
        </>
    );
}