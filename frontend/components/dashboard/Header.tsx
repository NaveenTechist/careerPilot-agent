"use client";

import { useState, useEffect, useCallback } from "react";
import { Menu, Search, Bell, User } from "lucide-react";
import CommandPalette from "./CommandPalette";

type Props = {
    onMenuToggle?: () => void;
};

export default function Header({ onMenuToggle }: Props) {
    const [scrolled, setScrolled] = useState(false);
    const [paletteOpen, setPaletteOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 10);
        window.addEventListener("scroll", handleScroll, { passive: true });
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    // Global keyboard shortcut ⌘K / Ctrl+K
    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if ((e.metaKey || e.ctrlKey) && e.key === "k") {
                e.preventDefault();
                setPaletteOpen(true);
            }
        };
        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, []);

    return (
        <>
            <header
                className={`sticky top-0 z-30 glass-header transition-all duration-300 ${
                    scrolled ? "py-2.5 shadow-lg shadow-slate-950/30" : "py-3.5"
                }`}
            >
                <div className="flex items-center justify-between px-4 sm:px-6">
                    {/* Left: Hamburger (mobile only) + Search */}
                    <div className="flex items-center gap-3">
                        {/* Mobile hamburger */}
                        {onMenuToggle && (
                            <button
                                onClick={onMenuToggle}
                                className="lg:hidden rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white transition-colors cursor-pointer"
                                aria-label="Open menu"
                            >
                                <Menu className="w-5 h-5" />
                            </button>
                        )}

                        {/* Mobile brand */}
                        <h1 className="lg:hidden text-sm font-extrabold tracking-tight text-white mr-2">
                            Career<span className="text-blue-400">Pilot</span>
                        </h1>

                        {/* Search trigger */}
                        <button
                            onClick={() => setPaletteOpen(true)}
                            className="hidden sm:flex items-center gap-2.5 rounded-xl glass-search px-4 py-2 text-sm text-slate-500 hover:text-slate-300 transition-colors cursor-pointer min-w-[220px]"
                        >
                            <Search className="w-4 h-4 shrink-0" />
                            <span className="text-xs">Search...</span>
                            <kbd className="ml-auto rounded-md border border-slate-700 bg-slate-800/60 px-1.5 py-0.5 text-[10px] text-slate-500 font-mono">
                                ⌘K
                            </kbd>
                        </button>
                    </div>

                    {/* Right: Notifications + Avatar */}
                    <div className="flex items-center gap-2.5">
                        {/* Search icon on mobile */}
                        <button
                            onClick={() => setPaletteOpen(true)}
                            className="sm:hidden rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white transition-colors cursor-pointer"
                            aria-label="Search"
                        >
                            <Search className="w-4.5 h-4.5" />
                        </button>

                        {/* Notifications */}
                        <button
                            className="relative rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white transition-colors cursor-pointer"
                            aria-label="Notifications"
                        >
                            <Bell className="w-4.5 h-4.5" />
                        </button>

                        {/* Avatar */}
                        <div className="relative flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-blue-600 to-indigo-600 text-white text-xs font-bold shadow-md">
                            U
                            <span className="absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full bg-emerald-500 ring-2 ring-slate-950" />
                        </div>
                    </div>
                </div>
            </header>

            <CommandPalette open={paletteOpen} onClose={() => setPaletteOpen(false)} />
        </>
    );
}