const steps = [

    "Resume",

    "Job",

    "Matching",

    "Automation",

];

export default function ProgressStepper({

    session,

}: any) {

    const completed = [

        session?.resume?.uploaded,

        session?.job?.uploaded,

        session?.status ===
        "READY_FOR_MATCHING",

        false,

    ];

    return (

        <div
            className="
            rounded-xl
            bg-slate-900
            p-6
            "
        >

            <div
                className="
                flex
                justify-between
                "
            >

                {

                    steps.map(

                        (

                            step,

                            i,

                        ) => (

                            <div
                                key={step}
                                className="flex flex-col items-center"
                            >

                                <div

                                    className={`

                                    h-12

                                    w-12

                                    rounded-full

                                    flex

                                    items-center

                                    justify-center

                                    font-bold

                                    ${completed[i]

                                            ?

                                            "bg-emerald-500 text-white"

                                            :

                                            "bg-slate-700 text-slate-400"

                                        }

                                    `}

                                >

                                    {

                                        completed[i]

                                            ?

                                            "✓"

                                            :

                                            i + 1

                                    }

                                </div>

                                <span
                                    className="
                                    mt-3
                                    text-slate-300
                                    "
                                >

                                    {step}

                                </span>

                            </div>

                        )

                    )

                }

            </div>

        </div>

    );

}