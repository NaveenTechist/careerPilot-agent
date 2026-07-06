export default function Header() {

    return (

        <header
            className="
            border-b
            border-slate-800
            bg-slate-900
            "
        >

            <div
                className="
                mx-auto
                flex
                max-w-7xl
                items-center
                justify-between
                px-8
                py-5
                "
            >

                <div>

                    <h1
                        className="
                        text-3xl
                        font-bold
                        text-white
                        "
                    >

                        CareerPilot AI

                    </h1>

                    <p
                        className="
                        mt-1
                        text-slate-400
                        "
                    >

                        AI Powered Job Application Agent

                    </p>

                </div>

            </div>

        </header>

    );

}