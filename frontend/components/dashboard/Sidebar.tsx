"use client";

import { LayoutDashboard, FolderOpen, User, Settings, LogOut, X } from "lucide-react";

type View = "dashboard" | "applications" | "profile" | "settings";

type Props = {
    activeView: View;
    onNavigate: (view: View) => void;
};

const NAV_ITEMS: { icon: typeof LayoutDashboard; label: string; view: View }[] = [
    { icon: LayoutDashboard, label: "Dashboard", view: "dashboard" },
    { icon: FolderOpen, label: "Applications", view: "applications" },
    { icon: User, label: "Profile", view: "profile" },
    { icon: Settings, label: "Settings", view: "settings" },
];

export default function Sidebar({ activeView, onNavigate }: Props) {
    return (
        <aside className="hidden lg:flex flex-col w-[220px] shrink-0 border-r border-slate-800/60 bg-slate-950/40 h-full">
            {/* Logo */}
            <div className="px-5 py-5 border-b border-slate-800/40">
                <h1 className="text-base font-extrabold tracking-tight text-white">
                    Career<span className="text-blue-400">Pilot</span>
                </h1>
            </div>

            {/* Nav items */}
            <nav className="flex-1 px-3 py-4 space-y-1">
                {NAV_ITEMS.map((item) => {
                    const isActive = activeView === item.view;
                    return (
                        <button
                            key={item.view}
                            onClick={() => onNavigate(item.view)}
                            className={`w-full flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-150 cursor-pointer ${
                                isActive
                                    ? "bg-blue-600/10 text-blue-400 border border-blue-500/15"
                                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50 border border-transparent"
                            }`}
                            aria-label={item.label}
                            aria-current={isActive ? "page" : undefined}
                        >
                            <item.icon className="w-4 h-4 shrink-0" />
                            {item.label}
                        </button>
                    );
                })}
            </nav>

            {/* Bottom section */}
            <div className="px-3 pb-4 border-t border-slate-800/40 pt-3">
                <button className="w-full flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-slate-500 hover:text-red-400 hover:bg-red-500/5 transition-all cursor-pointer">
                    <LogOut className="w-4 h-4 shrink-0" />
                    Logout
                </button>
            </div>
        </aside>
    );
}

/* ----------- Mobile Sidebar ----------- */

type MobileProps = Props & {
    isOpen: boolean;
    onClose: () => void;
};

export function MobileSidebar({ isOpen, onClose, activeView, onNavigate }: MobileProps) {
    if (!isOpen) return null;

    return (
        <>
            {/* Backdrop */}
            <div
                className="fixed inset-0 z-40 bg-slate-950/70 backdrop-blur-sm lg:hidden"
                onClick={onClose}
            />

            {/* Panel */}
            <div className="fixed inset-y-0 left-0 z-50 w-[260px] bg-slate-950 border-r border-slate-800 shadow-2xl flex flex-col lg:hidden animate-slide-in-left">
                {/* Mobile Header */}
                <div className="flex items-center justify-between px-5 py-4 border-b border-slate-800/50">
                    <h1 className="text-base font-extrabold tracking-tight text-white">
                        Career<span className="text-blue-400">Pilot</span>
                    </h1>
                    <button
                        onClick={onClose}
                        className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white transition-colors cursor-pointer"
                        aria-label="Close menu"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Nav */}
                <nav className="flex-1 px-3 py-4 space-y-1">
                    {NAV_ITEMS.map((item) => {
                        const isActive = activeView === item.view;
                        return (
                            <button
                                key={item.view}
                                onClick={() => {
                                    onNavigate(item.view);
                                    onClose();
                                }}
                                className={`w-full flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium transition-all cursor-pointer ${
                                    isActive
                                        ? "bg-blue-600/10 text-blue-400 border border-blue-500/15"
                                        : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50 border border-transparent"
                                }`}
                            >
                                <item.icon className="w-4.5 h-4.5 shrink-0" />
                                {item.label}
                            </button>
                        );
                    })}
                </nav>

                {/* Logout */}
                <div className="px-3 pb-4 border-t border-slate-800/40 pt-3">
                    <button className="w-full flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-500 hover:text-red-400 hover:bg-red-500/5 transition-all cursor-pointer">
                        <LogOut className="w-4.5 h-4.5 shrink-0" />
                        Logout
                    </button>
                </div>
            </div>
        </>
    );
}
