"use client";

import ScoreCircle from "./dashboard/ScoreCircle";

import SkillBadge from "./dashboard/SkillBadge";

import ActionButtons from "@/components/dashboard/ActionButtons";

import { MatchResult } from "@/types/match";

type Props = {

    data: MatchResult;

};

export default function MatchResultCard({

    data,

}: Props) {

    const result = data.result;

    return (

        <div className="mx-auto mt-10 max-w-6xl rounded-3xl border border-white/10 bg-slate-900 p-8 shadow-2xl">

            <div className="flex items-center justify-between">

                <div>

                    <h2 className="text-3xl font-bold text-white">

                        AI Match Analysis

                    </h2>

                    <p className="mt-2 text-slate-400">

                        {result.overall_level}

                    </p>

                </div>

                <ScoreCircle

                    score={result.score}

                />

            </div>

            <div className="mt-8 grid gap-8 lg:grid-cols-2">

                <div>

                    <h3 className="mb-3 text-xl font-semibold text-emerald-400">

                        Matched Skills

                    </h3>

                    <div className="flex flex-wrap gap-2">

                        {result.matched_skills.map(

                            (skill) => (

                                <SkillBadge

                                    key={skill}

                                    text={skill}

                                    type="success"

                                />

                            )

                        )}

                    </div>

                </div>

                <div>

                    <h3 className="mb-3 text-xl font-semibold text-red-400">

                        Missing Skills

                    </h3>

                    <div className="flex flex-wrap gap-2">

                        {result.missing_skills.map(

                            (skill) => (

                                <SkillBadge

                                    key={skill}

                                    text={skill}

                                    type="danger"

                                />

                            )

                        )}

                    </div>

                </div>

            </div>

            <div className="mt-8">

                <h3 className="text-xl font-semibold text-white">

                    AI Recommendation

                </h3>

                <p className="mt-3 text-slate-300 leading-8">

                    {result.recommendation}

                </p>

            </div>

            <ActionButtons

                matchId={data.match_id}

                shouldApply={result.should_apply}

            />

        </div>

    );

}