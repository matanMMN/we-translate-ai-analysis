"use client"

import {ReactNode, useEffect} from "react";
// import {toast} from "sonner";

export default function SSEListener({children}: { children: ReactNode }) {

    useEffect(() => {
        const eventSource = new EventSource("/api/stream");

        eventSource.onmessage = function (event) {
            const data = JSON.parse(event.data)
            console.log("Received data from server:", data);

            // toast.success(`Data received from server! ${Object.values(data).toString()}`)
        };

        eventSource.onerror = function (event) {
            console.error("Error from server:", event);
            eventSource.close()
        };

        return () => {
            eventSource.close();
        }
    }, []);

    return children
}