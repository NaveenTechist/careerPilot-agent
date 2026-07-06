"use client";

import { useState } from "react";

import {

    proceedMatch,

    cancelMatch,

} from "@/services/matching";

import Loading from "./Loading";

import Toast from "./Toast";

import { useToast } from "@/hooks/useToast";

type Props = {

    matchId: string;

    shouldApply: boolean;

};

export default function ActionButtons({

    matchId,

    shouldApply,

}: Props) {

    const [

        loading,

        setLoading,

    ] = useState(false);

    const {

        visible,

        message,

        type,

        showToast,

    } = useToast();

    async function proceed() {

        try {

            setLoading(true);

            await proceedMatch(

                matchId,

            );

            showToast(

                "Application approved. Preparing browser automation.",

                "success",

            );

        }

        catch {

            showToast(

                "Unable to proceed.",

                "error",

            );

        }

        finally {

            setLoading(false);

        }

    }

    async function cancel() {

        try {

            setLoading(true);

            await cancelMatch(

                matchId,

            );

            showToast(

                "Application cancelled.",

                "warning",

            );

        }

        catch {

            showToast(

                "Unable to cancel.",

                "error",

            );

        }

        finally {

            setLoading(false);

        }

    }

    return (

        <>

            {loading && (

                <Loading

                    text="Updating Match..."

                />

            )}

            <Toast

                visible={visible}

                message={message}

                type={type}

            />

            <div className="mt-10 flex justify-end gap-5">

                <button

                    onClick={cancel}

                    className="rounded-xl border border-red-500 px-8 py-3 font-semibold text-red-400 transition hover:bg-red-600 hover:text-white"

                >

                    Cancel

                </button>

                <button

                    onClick={proceed}

                    disabled={!shouldApply}

                    className="rounded-xl bg-blue-600 px-8 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-700"

                >

                    Proceed

                </button>

            </div>

        </>

    );

}