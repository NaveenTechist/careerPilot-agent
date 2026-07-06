type Props = {

    visible: boolean;

    message: string;

    type:

    | "success"

    | "error"

    | "warning";

};

export default function Toast({

    visible,

    message,

    type,

}: Props) {

    if (!visible) return null;

    const color =

        type === "success"

            ? "bg-emerald-600"

            : type === "error"

                ? "bg-red-600"

                : "bg-yellow-500";

    return (

        <div

            className={`fixed right-8 top-8 z-50 rounded-xl px-5 py-4 text-white shadow-xl ${color}`}

        >

            {message}

        </div>

    );

}