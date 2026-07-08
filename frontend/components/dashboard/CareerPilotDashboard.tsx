"use client";

import { useEffect, useState, useCallback, useMemo } from "react";
import Header from "./Header";
import Sidebar, { MobileSidebar } from "./Sidebar";
import Notification from "./Notification";
import NewApplicationModal from "./NewApplicationModal";
import ApplicationCard, { type ApplicationSummary } from "./ApplicationCard";
import ApplicationDrawer from "./ApplicationDrawer";
import SearchBar from "./SearchBar";
import EmptyState from "./EmptyState";
import LoadingSkeleton from "./LoadingSkeleton";
import { useNotification } from "@/hooks/useNotification";
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

    const { notify, message, open, dismiss } = useNotification();

    // ── Load Applications ──
    const loadApplications = useCallback(async () => {
        setAppsLoading(true);
        try {
            const data = await getApplications();
            setApplications(data);
        } catch (err: any) {
            console.error("Failed to load applications:", err);
        } finally {
            setAppsLoading(false);
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

    // ── Handlers ──
    function handleNewApplicationSuccess() {
        setModalOpen(false);
        notify("Application created.");
        loadApplications();
    }

    function handleCardClick(id: string) {
        setSelectedAppId(id);
    }

    function handleDrawerStatusChange() {
        notify("Application status updated.");
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
                        className="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-500 px-5 py-3 text-sm font-bold text-white shadow-lg shadow-blue-950/40 transition-all duration-200 active:translate-y-0.5 cursor-pointer sm:sticky sm:top-20 z-10"
                        id="new-application-btn"
                    >
                        <Plus className="w-4 h-4" />
                        New Application
                    </button>
                </div>

                {/* Stats Row (Dashboard only) */}
                {activeView === "dashboard" && (
                    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                        <div className="rounded-2xl bg-slate-900/60 border border-slate-800/50 p-4">
                            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total</p>
                            <p className="mt-1.5 text-2xl font-extrabold text-white tabular-nums">{totalCount}</p>
                        </div>
                        <div className="rounded-2xl bg-slate-900/60 border border-slate-800/50 p-4">
                            <p className="text-xs font-semibold text-blue-400/70 uppercase tracking-wider">Pending</p>
                            <p className="mt-1.5 text-2xl font-extrabold text-blue-400 tabular-nums">{pendingCount}</p>
                        </div>
                        <div className="rounded-2xl bg-slate-900/60 border border-slate-800/50 p-4">
                            <p className="text-xs font-semibold text-emerald-400/70 uppercase tracking-wider">Proceeded</p>
                            <p className="mt-1.5 text-2xl font-extrabold text-emerald-400 tabular-nums">{proceededCount}</p>
                        </div>
                        <div className="rounded-2xl bg-slate-900/60 border border-slate-800/50 p-4">
                            <p className="text-xs font-semibold text-purple-400/70 uppercase tracking-wider">Completed</p>
                            <p className="mt-1.5 text-2xl font-extrabold text-purple-400 tabular-nums">{completedCount}</p>
                        </div>
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
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                            {filteredApplications.map((app) => (
                                <ApplicationCard
                                    key={app.id}
                                    application={app}
                                    onClick={handleCardClick}
                                />
                            ))}
                        </div>
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
                <Notification open={open} message={message} onClose={dismiss} />

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
        </div>
    );
}