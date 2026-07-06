type Props = {

    text: string;

    type: "success" | "danger";

};
export default function SkillBadge({
    text,
    type,
}: Props) {
    const style =
        type === "success"
            ? "bg-emerald-500/20 text-emerald-300 border-emerald-500"
            : "bg-red-500/20 text-red-300 border-red-500";
    return (
        <span
            className={`rounded-full border px-3 py-1 text-sm ${style}`}
        >
            {text}
        </span>
    );
}