import { useState, useRef } from "react";

export function useNotification() {
    const [message, setMessage] = useState("");
    const [open, setOpen] = useState(false);
    const timerRef = useRef<NodeJS.Timeout | null>(null);

    function notify(text: string) {
        // Clear any existing timer
        if (timerRef.current) {
            clearTimeout(timerRef.current);
        }

        setMessage(text);
        setOpen(true);

        // Auto-dismiss after 4 seconds
        timerRef.current = setTimeout(() => {
            setOpen(false);
            timerRef.current = null;
        }, 4000);
    }

    function dismiss() {
        if (timerRef.current) {
            clearTimeout(timerRef.current);
            timerRef.current = null;
        }
        setOpen(false);
    }

    return {
        message,
        open,
        notify,
        dismiss
    };
}