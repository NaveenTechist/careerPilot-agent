"use client";

import ScoreCircle from "./ScoreCircle";
import SkillBadge from "./SkillBadge";
import ActionButtons from "./ActionButtons";

type Props = {
    result: any;
    onProceed: () => void;
    onCancel: () => void;
};

export default function MatchCard({
    result,
    onProceed,
    onCancel,
}: Props) {

    if (!result) return null;

    return (

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8 shadow-xl">

            <div className="flex items-center justify-between">

                <div>

                    <h2 className="text-3xl font-bold text-white">

                        AI Match Result

                    </h2>

                    <p className="mt-2 text-slate-400">

                        Resume vs Job Analysis

                    </p>

                </div>

                <ScoreCircle score={result.score} />

            </div>

            <div className="mt-8 grid grid-cols-2 gap-8">

                <div>

                    <h3 className="mb-3 font-semibold text-emerald-400">

                        Matched Skills

                    </h3>

                    <div className="flex flex-wrap gap-2">

                        {result.matched_skills.map((skill: string) => (

                            <SkillBadge
                                key={skill}
                                text={skill}
                                type="success"
                            />

                        ))}

                    </div>

                </div>

                <div>

                    <h3 className="mb-3 font-semibold text-red-400">

                        Missing Skills

                    </h3>

                    <div className="flex flex-wrap gap-2">

                        {result.missing_skills.map((skill: string) => (

                            <SkillBadge
                                key={skill}
                                text={skill}
                                type="danger"
                            />

                        ))}

                    </div>

                </div>

            </div>

            <div className="mt-8">

                <h3 className="font-semibold text-blue-400">

                    Recommendation

                </h3>

                <p className="mt-3 leading-7 text-slate-300">

                    {result.recommendation}

                </p>

            </div>

            <ActionButtons

                matchId={result.id}

                shouldApply={result.should_apply}

                onProceed={onProceed}

                onCancel={onCancel}

            />

        </div>

    );

}