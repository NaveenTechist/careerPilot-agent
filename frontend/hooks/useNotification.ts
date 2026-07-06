import { useState } from "react";

export function useNotification() {

    const [

        message,

        setMessage,

    ] = useState("");

    const [

        open,

        setOpen,

    ] = useState(false);

    function notify(
        text: string
    ) {

        setMessage(text);

        setOpen(true);

        setTimeout(() => {

            setOpen(false);

        }, 3000);

    }

    return {

        message,

        open,

        notify,

    };

}