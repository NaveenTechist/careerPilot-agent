type Props = {
    status: string;
};

const STATUS_MAP: Record<string, { label: string; classes: string }> = {
    READY: {
        label: "Pending",
        classes: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    },
    MATCH_PENDING: {
        label: "Pending",
        classes: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    },
    PENDING: {
        label: "Pending",
        classes: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    },
    CANCELLED: {
        label: "Cancelled",
        classes: "bg-red-500/10 text-red-400 border-red-500/20",
    },
    PROCEEDED: {
        label: "Proceeded",
        classes: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    },
    COMPLETED: {
        label: "Completed",
        classes: "bg-purple-500/10 text-purple-400 border-purple-500/20",
    },
};

export default function StatusBadge({ status }: Props) {
    const config = STATUS_MAP[status] || STATUS_MAP.PENDING;
    return (
        <span
            className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-[11px] font-bold uppercase tracking-wider select-none ${config.classes}`}
        >
            {config.label}
        </span>
    );
}
