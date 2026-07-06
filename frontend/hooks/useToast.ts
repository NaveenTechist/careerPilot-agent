"use client";

import { useState } from "react";

export type ToastType =

    | "success"

    | "error"

    | "warning";

export function useToast() {

    const [

        message,

        setMessage,

    ] = useState("");

    const [

        type,

        setType,

    ] = useState<ToastType>("success");

    const [

        visible,

        setVisible,

    ] = useState(false);

    function showToast(

        msg: string,

        toastType: ToastType,

    ) {

        setMessage(msg);

        setType(toastType);

        setVisible(true);

        setTimeout(() => {

            setVisible(false);

        }, 3500);

    }

    return {

        message,

        type,

        visible,

        showToast,

    };

}