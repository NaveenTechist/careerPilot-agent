type Props = {

    score: number;

};

export default function ScoreCircle({

    score,

}: Props) {

    const color =

        score >= 90

            ? "text-emerald-400"

            : score >= 75

                ? "text-blue-400"

                : score >= 60

                    ? "text-yellow-400"

                    : "text-red-400";

    return (

        <div

            className={`mx-auto flex h-44 w-44 items-center justify-center rounded-full border-[10px] border-current ${color}`}

        >

            <div className="text-center">

                <p className="text-5xl font-bold">

                    {score}

                </p>

                <p className="text-sm">

                    %

                </p>

            </div>

        </div>

    );

}