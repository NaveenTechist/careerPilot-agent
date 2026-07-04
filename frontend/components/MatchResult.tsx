"use client";

type Props = {

    result: any;

    onProceed: () => void;

    onCancel: () => void;
};

export default function MatchResult({

    result,

    onProceed,

    onCancel,

}: Props) {

    if (!result) return null;

    return (

        <div className="mt-8 rounded-lg border p-6">

            <h2 className="text-2xl font-bold">

                Match Score

            </h2>

            <p className="mt-3 text-5xl font-bold text-blue-600">

                {result.score}%

            </p>

            <div className="mt-6">

                <h3 className="font-semibold">

                    Matched Skills

                </h3>

                <ul>

                    {result.matched_skills.map(

                        (skill: string) => (

                            <li key={skill}>

                                ✅ {skill}

                            </li>

                        )

                    )}

                </ul>

            </div>

            <div className="mt-6">

                <h3 className="font-semibold">

                    Missing Skills

                </h3>

                <ul>

                    {result.missing_skills.map(

                        (skill: string) => (

                            <li key={skill}>

                                ❌ {skill}

                            </li>

                        )

                    )}

                </ul>

            </div>

            <div className="mt-6">

                <h3 className="font-semibold">

                    Recommendation

                </h3>

                <p>

                    {result.recommendation}

                </p>

            </div>

            <div className="mt-8 flex gap-4">

                <button
                    onClick={onProceed}
                    className="rounded bg-green-600 px-6 py-2 text-white"
                >

                    Proceed

                </button>

                <button
                    onClick={onCancel}
                    className="rounded bg-red-600 px-6 py-2 text-white"
                >

                    Cancel

                </button>

            </div>

        </div>

    );

}