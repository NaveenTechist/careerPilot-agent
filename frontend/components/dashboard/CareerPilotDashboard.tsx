"use client";

import { useEffect, useState } from "react";

import ResumeCard from "./ResumeCard";
import JobCard from "./JobCard";
import MatchCard from "./MatchCard";
import ProgressStepper from "./ProgressStepper";
import Header from "./Header";
import Notification from "./Notification";

import { getSession } from "@/services/session";
import { uploadResume } from "@/services/resume";
import { analyzeJob } from "@/services/job";
import {
    matchResume,
    proceedMatch,
    cancelMatch,
} from "@/services/matching";

import { useNotification } from "@/hooks/useNotification";

export default function CareerPilotDashboard() {

    const [session, setSession] = useState<any>(null);

    const [match, setMatch] = useState<any>(null);

    const [loading, setLoading] = useState(false);

    const { notify, message, open } =
        useNotification();

    async function refreshSession() {

        const data = await getSession();

        setSession(data);

    }

    useEffect(() => {

        refreshSession();

    }, []);

    async function handleResume(
        file: File,
    ) {

        setLoading(true);

        try {

            await uploadResume(file);

            notify(
                "Resume uploaded successfully."
            );
            await refreshSession();
        }
        catch (e: any) {
            notify(e.message);
        }
        finally {
            setLoading(false);
        }
    }

    async function handleJob(
        url: string,
    ) {
        setLoading(true);
        try {
            await analyzeJob(url);
            notify(
                "Job analyzed successfully."
            );
            await refreshSession();
        }
        catch (e: any) {
            notify(e.message);
        }
        finally {
            setLoading(false);
        }
    }

    async function handleMatch() {
        setLoading(true);
        try {
            const result =
                await matchResume();
            setMatch(result);
            notify(
                "Matching completed."
            );
        }
        catch (e: any) {
            notify(e.message);
        }
        finally {
            setLoading(false);
        }
    }

    async function handleProceed() {
        await proceedMatch(match.match_id);
        console.log("matching results", match)
        console.log(match.match_id)
        notify(
            "Browser automation started."
        );
    }
    async function handleCancel() {

        await cancelMatch(match.match_id);
        notify(
            "Application cancelled."
        );
        setMatch(null);
    }
    return (

        <main className="min-h-screen bg-slate-950">

            <Header />

            <Notification
                open={open}
                message={message}
            />

            <div className="mx-auto max-w-7xl p-8 space-y-8">

                <ProgressStepper
                    session={session}
                />

                <ResumeCard
                    session={session}
                    onUpload={handleResume}
                />

                <JobCard
                    session={session}
                    onAnalyze={handleJob}
                />

                {

                    session?.status ===
                    "READY_FOR_MATCHING"

                    &&

                    <button

                        onClick={handleMatch}

                        className="rounded-xl
                        bg-blue-600
                        px-6
                        py-3
                        font-semibold
                        text-white"

                    >

                        Analyze Match

                    </button>

                }

                {

                    match &&

                    <MatchCard

                        result={match}

                        onProceed={
                            handleProceed
                        }

                        onCancel={
                            handleCancel
                        }

                    />

                }

            </div>

        </main>

    );

}