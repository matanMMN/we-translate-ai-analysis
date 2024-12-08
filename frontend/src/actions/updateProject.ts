"use server"

import { getUser } from "@/lib/AuthGuard";
import { serverUrl } from "@/lib/functions"


interface ProjectUpdateProps {
    projectId: string,
    targetFileId: string,
}

export async function updateTargetFile({ projectId, targetFileId }: ProjectUpdateProps) {

    const session = await getUser()
    console.log(projectId, targetFileId, session)
    const res = await fetch(`${serverUrl}/jobs/${projectId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session!.accessToken}`,
        },
        body: JSON.stringify({ target_file_id: targetFileId })
    })
    const isUpdateSuccess = await res.json();
    console.log(isUpdateSuccess)
    if (isUpdateSuccess.status_code !== 200)
        throw new Error("Project update failed")

}