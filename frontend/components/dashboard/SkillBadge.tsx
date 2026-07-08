type Props = {
    text: string;
    type: "success" | "danger" | "warning" | "info";
};

export default function SkillBadge({ text, type }: Props) {
    const getStyles = () => {
        switch (type) {
            case "success":
                return "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/15";
            case "danger":
                return "bg-red-500/10 text-red-400 border-red-500/20 hover:bg-red-500/15";
            case "warning":
                return "bg-amber-500/10 text-amber-400 border-amber-500/20 hover:bg-amber-500/15";
            case "info":
            default:
                return "bg-blue-500/10 text-blue-400 border-blue-500/20 hover:bg-blue-500/15";
        }
    };

    return (
        <span
            className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium tracking-wide transition-all duration-150 cursor-default select-none ${getStyles()}`}
        >
            {text}
        </span>
    );
}