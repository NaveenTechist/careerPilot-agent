type Props = {
    score: number;
};

export default function ScoreBadge({ score }: Props) {
    const getColors = () => {
        if (score >= 90) return "text-emerald-400 bg-emerald-500/10 border-emerald-500/20";
        if (score >= 75) return "text-blue-400 bg-blue-500/10 border-blue-500/20";
        if (score >= 60) return "text-amber-400 bg-amber-500/10 border-amber-500/20";
        return "text-red-400 bg-red-500/10 border-red-500/20";
    };

    return (
        <span
            className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-extrabold tabular-nums select-none ${getColors()}`}
        >
            {score}%
        </span>
    );
}
