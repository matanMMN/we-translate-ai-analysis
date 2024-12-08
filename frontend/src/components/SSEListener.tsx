"use client"

import { getFileMetaData } from "@/actions/updateProject";
import { ReactNode, useEffect } from "react";
import { toast } from "sonner";
// import { useAppDispatch } from "@/hooks/useAppDispatch";
// import { setTranslatedFile } from "@/store/slices/projectSlice";

export default function SSEListener({ children }: { children: ReactNode }) {


    // const dispatch = useAppDispatch()

    useEffect(() => {
        const eventSource = new EventSource("/api/stream");

        eventSource.onmessage = async function (event) {
            const response = JSON.parse(event.data)
            console.log("Received data from server:", response);
            toast.success(`${response?.translation_data ? 'New data received from server! Translated file is ready!' : 'Listening to server for incoming webhooks...'}`)


            if (!response?.translation_data)
                return
            console.log("response")
            console.log(response)
            const data = await getFileMetaData(response.translation_job_id)
            console.log("data")
            console.log(data)
            // if (data.success && data.mockBlob && data.blobType) {
            //     dispatch(setTranslatedFile({
            //         blob: data.mockBlob as unknown as Blob,
            //         type: data.blobType
            //     }))
            // } else {
            //     toast.error("Data couldn't be extracted")
            // }
            // console.log("All clients: ", clients)
            // if (response?.translation_data)
            //     try {
            //         await updateTargetFile({
            //             projectId: response.translation_job_id,
            //             targetFileId: response.translation_data.file_id,

            //         })
            //     } catch (e) {
            //         console.error("SSE reaction failed: ", e)
            //     }

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