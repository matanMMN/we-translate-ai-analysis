"use server"

import { getUser } from "@/lib/AuthGuard";
import { serverUrl } from "@/lib/functions"
import { revalidatePath } from "next/dist/server/web/spec-extension/revalidate";
import { toast } from "sonner";


interface ProjectUpdateProps {
    projectId: string,
    targetFileId: string,
}

export async function updateProjectData({ projectId, editedProject }: any) {
    const user = await getUser()
    if (!user)
        throw new Error("User authentication failed")

    try {
        const response = await fetch(`${serverUrl}/jobs/${projectId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${user?.accessToken}`,
            },
            body: JSON.stringify(editedProject),
        });
        console.log(response)
        if (!response.ok)
            throw new Error('Failed to update project');
        const updatedProject = await response.json();
        console.log(updatedProject)
        return updatedProject

    } catch (error) {
        console.error(error)
        toast("Failed to update project. Please try again.");
    }
}


export async function getFileMetaData(fileId: string) {
    const user = await getUser()
    if (!user)
        throw new Error("User authentication failed")
    const translatedFileRes = await fetch(`${serverUrl}/files/download/${fileId}`, {
        headers: {
            'Authorization': `Bearer ${user.accessToken}`,
        },
    })

    if (!translatedFileRes)
        return { success: false, error: 'Failed to process the file' }

    const arrayBuffer = await translatedFileRes.arrayBuffer();
    const encodedString = Buffer.from(arrayBuffer).toString('base64');


    revalidatePath(`/`);

    return {
        success: true,
        mockBlob: encodedString,
        blobType: "docx"
    };
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