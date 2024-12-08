"use client"

import { updateTargetFile } from "@/actions/updateProject";
import { ReactNode, useEffect } from "react";
import { toast } from "sonner";
import { clients } from "@/app/api/stream/route"

export default function SSEListener({ children }: { children: ReactNode }) {

    useEffect(() => {
        const eventSource = new EventSource("/api/stream");

        eventSource.onmessage = async function (event) {
            const response = JSON.parse(event.data)
            console.log("Received data from server:", response);
            toast.success(`New data received from server! ${response?.translation_data ? response.translation_data : ''}`)
            console.log("All clients: ", clients)
            if (response?.translation_data)
                try {
                    await updateTargetFile({
                        projectId: response.translation_job_id,
                        targetFileId: response.translation_data.file_id,

                    })
                } catch (e) {
                    console.error("SSE reaction failed: ", e)
                }

        };

        eventSource.onerror = function (event) {
            console.error("Error from server:", event);
            // eventSource.close() 
        };

        return () => {
            // eventSource.close();
        }
    }, []);

    return children
}