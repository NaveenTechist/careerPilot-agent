"use client";

import { useEffect, useState, useCallback, useMemo } from "react";
import { AnimatePresence, motion } from "framer-motion";
import Header from "./Header";
import Sidebar, { MobileSidebar } from "./Sidebar";
import NewApplicationModal from "./NewApplicationModal";
import ApplicationCard, { type ApplicationSummary } from "./ApplicationCard";
import ApplicationDrawer from "./ApplicationDrawer";
import SearchBar from "./SearchBar";
import EmptyState from "./EmptyState";
import LoadingSkeleton from "./LoadingSkeleton";
import { useAppToast } from "@/hooks/useAppToast";
import { getApplications } from "@/services/application";
import { Plus, FolderOpen, User, Settings } from "lucide-react";

type View = "dashboard" | "applications" | "profile" | "settings";
type Filter = "ALL" | "READY" | "CANCELLED" | "PROCEEDED" | "COMPLETED";
type Sort = "newest" | "oldest" | "score_high" | "score_low";

export default function CareerPilotDashboard() {
    // ── Core State ──
    const [activeView, setActiveView] = useState<View>("dashboard");
    const [applications, setApplications] = useState<ApplicationSummary[]>([]);
    const [appsLoading, setAppsLoading] = useState(true);

    // ── UI State ──
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [modalOpen, setModalOpen] = useState(false);
    const [selectedAppId, setSelectedAppId] = useState<string | null>(null);

    // ── Search / Filter / Sort State ──
    const [searchQuery, setSearchQuery] = useState("");
    const [filter, setFilter] = useState<Filter>("ALL");
    const [sort, setSort] = useState<Sort>("newest");

    const { toastSuccess, toastError, toastInfo } = useAppToast();

    // ── Load Applications ──
    const loadApplications = useCallback(async (silent = false) => {
        if (!silent) setAppsLoading(true);
        try {
            const data = await getApplications();
            setApplications(data);
        } catch (err: any) {
            console.error("Failed to load applications:", err);
        } finally {
            if (!silent) setAppsLoading(false);
        }
    }, []);

    useEffect(() => {
        loadApplications();
    }, [loadApplications]);

    // ── Filtered + Sorted Applications ──
    const filteredApplications = useMemo(() => {
        let result = [...applications];

        // Filter by status
        if (filter !== "ALL") {
            result = result.filter((app) => app.status === filter);
        }

        // Search by company / title / status
        if (searchQuery.trim()) {
            const q = searchQuery.toLowerCase();
            result = result.filter(
                (app) =>
                    app.title?.toLowerCase().includes(q) ||
                    app.status?.toLowerCase().includes(q)
            );
        }

        // Sort
        switch (sort) {
            case "newest":
                result.sort((a, b) => new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime());
                break;
            case "oldest":
                result.sort((a, b) => new Date(a.created_at || 0).getTime() - new Date(b.created_at || 0).getTime());
                break;
            case "score_high":
                result.sort((a, b) => b.score - a.score);
                break;
            case "score_low":
                result.sort((a, b) => a.score - b.score);
                break;
        }

        return result;
    }, [applications, filter, searchQuery, sort]);

    const [highlightedAppId, setHighlightedAppId] = useState<string | null>(null);

    // ── Handlers ──
    async function handleNewApplicationSuccess(newAppId?: string) {
        setModalOpen(false);
        toastSuccess("Application created successfully.");
        await loadApplications(true);

        if (newAppId) {
            setHighlightedAppId(newAppId);
            setTimeout(() => {
                const el = document.querySelector(`[data-app-id="${newAppId}"]`);
                if (el) {
                    el.scrollIntoView({ behavior: "smooth", block: "center" });
                }
            }, 100);

            setTimeout(() => {
                setHighlightedAppId(null);
            }, 2500);
        }
    }

    function handleCardClick(id: string) {
        setSelectedAppId(id);
    }

    function handleDrawerStatusChange() {
        toastSuccess("Application status updated.");
        loadApplications();
    }

    // ── Stat Counts ──
    const totalCount = applications.length;
    const pendingCount = applications.filter((a) => a.status === "READY" || a.status === "MATCH_PENDING" || a.status === "PENDING").length;
    const proceededCount = applications.filter((a) => a.status === "PROCEEDED").length;
    const completedCount = applications.filter((a) => a.status === "COMPLETED").length;

    // ── Render Page Content ──
    function renderContent() {
        if (activeView === "profile") {
            return (
                <div className="flex flex-col items-center justify-center py-20 text-center">
                    <User className="w-12 h-12 text-slate-700 mb-4" />
                    <h3 className="text-lg font-bold text-slate-300">Profile</h3>
                    <p className="text-sm text-slate-500 mt-1">Coming soon in a future release.</p>
                </div>
            );
        }
        if (activeView === "settings") {
            return (
                <div className="flex flex-col items-center justify-center py-20 text-center">
                    <Settings className="w-12 h-12 text-slate-700 mb-4" />
                    <h3 className="text-lg font-bold text-slate-300">Settings</h3>
                    <p className="text-sm text-slate-500 mt-1">Coming soon in a future release.</p>
                </div>
            );
        }

        // ── Dashboard / Applications View ──
        return (
            <div className="space-y-8">
                {/* Page Title + New Application Button */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                        <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                            {activeView === "applications" ? "Applications" : "Dashboard"}
                        </h2>
                        <p className="text-sm text-slate-500 mt-1">
                            {activeView === "applications"
                                ? "Manage and track all your job applications"
                                : "Overview of your career applications pipeline"
                            }
                        </p>
                    </div>
                    <button
                        onClick={() => setModalOpen(true)}
                        className="hidden sm:inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-500 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-blue-950/40 transition-all duration-200 active:translate-y-0.5 cursor-pointer"
                        id="new-application-btn"
                    >
                        <Plus className="w-4 h-4" />
                        New Application
                    </button>
                </div>

                {/* Stats Row (Dashboard only) */}
                {activeView === "dashboard" && (
                    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                        {[
                            { label: "Total", value: totalCount, color: "text-white", labelColor: "text-slate-500" },
                            { label: "Pending", value: pendingCount, color: "text-blue-400", labelColor: "text-blue-400/70" },
                            { label: "Proceeded", value: proceededCount, color: "text-emerald-400", labelColor: "text-emerald-400/70" },
                            { label: "Completed", value: completedCount, color: "text-purple-400", labelColor: "text-purple-400/70" },
                        ].map((stat, idx) => (
                            <motion.div
                                key={stat.label}
                                initial={{ opacity: 0, y: 16 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: idx * 0.08, duration: 0.35, ease: "easeOut" }}
                                className="rounded-2xl bg-slate-900/60 border border-slate-800/50 p-4 hover:border-slate-700/60 hover:bg-slate-900/80 transition-all duration-200"
                            >
                                <p className={`text-xs font-semibold uppercase tracking-wider ${stat.labelColor}`}>{stat.label}</p>
                                <p className={`mt-1.5 text-2xl font-extrabold tabular-nums ${stat.color}`}>{stat.value}</p>
                            </motion.div>
                        ))}
                    </div>
                )}

                {/* Search + Filters */}
                <SearchBar
                    query={searchQuery}
                    onQueryChange={setSearchQuery}
                    filter={filter}
                    onFilterChange={setFilter}
                    sort={sort}
                    onSortChange={setSort}
                />

                {/* Past Applications Section */}
                <div>
                    <div className="flex items-center gap-2 mb-5">
                        <FolderOpen className="w-4 h-4 text-slate-500" />
                        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest">
                            {activeView === "applications" ? "All Applications" : "Past Applications"}
                        </h3>
                        <span className="ml-1 rounded-full bg-slate-800 px-2 py-0.5 text-[11px] font-bold text-slate-400 tabular-nums">
                            {filteredApplications.length}
                        </span>
                    </div>

                    {appsLoading ? (
                        <LoadingSkeleton />
                    ) : filteredApplications.length === 0 && applications.length === 0 ? (
                        <EmptyState onNewApplication={() => setModalOpen(true)} />
                    ) : filteredApplications.length === 0 ? (
                        <div className="text-center py-12">
                            <p className="text-sm text-slate-500">
                                No applications match your search or filter.
                            </p>
                        </div>
                    ) : (
                        <motion.div 
                            layout
                            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5"
                        >
                            <AnimatePresence mode="popLayout">
                                {filteredApplications.map((app) => (
                                    <ApplicationCard
                                        key={app.id}
                                        application={app}
                                        onClick={handleCardClick}
                                        highlighted={app.id === highlightedAppId}
                                    />
                                ))}
                            </AnimatePresence>
                        </motion.div>
                    )}
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#020617] text-[#f8fafc] flex">
            {/* Desktop Sidebar */}
            <Sidebar activeView={activeView} onNavigate={setActiveView} />

            {/* Mobile Sidebar */}
            <MobileSidebar
                isOpen={mobileMenuOpen}
                onClose={() => setMobileMenuOpen(false)}
                activeView={activeView}
                onNavigate={setActiveView}
            />

            {/* Main Area */}
            <div className="flex-1 flex flex-col min-w-0">
                <Header onMenuToggle={() => setMobileMenuOpen((o) => !o)} />

                {/* Page Content */}
                <main className="flex-1 px-4 py-6 sm:px-6 lg:px-8 max-w-7xl w-full mx-auto">
                    {renderContent()}
                </main>
            </div>

            {/* New Application Modal */}
            <NewApplicationModal
                isOpen={modalOpen}
                onClose={() => setModalOpen(false)}
                onSuccess={handleNewApplicationSuccess}
            />

            {/* Application Details Drawer */}
            <ApplicationDrawer
                applicationId={selectedAppId}
                onClose={() => setSelectedAppId(null)}
                onStatusChange={handleDrawerStatusChange}
            />

            {/* Mobile FAB — New Application */}
            <button
                onClick={() => setModalOpen(true)}
                className="fixed bottom-6 right-6 z-30 flex sm:hidden h-14 w-14 items-center justify-center rounded-full bg-blue-600 hover:bg-blue-500 text-white shadow-2xl shadow-blue-950/60 active:scale-95 transition-all duration-150 cursor-pointer"
                aria-label="New Application"
            >
                <Plus className="w-6 h-6" />
            </button>
        </div>
    );
}