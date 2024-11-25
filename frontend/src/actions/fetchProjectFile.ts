'use server'
import {serverUrl} from "@/lib/functions";
import {getUser} from "@/lib/AuthGuard";
//
// interface ProjectFileResponse {
//     content: string
//     type: string
//     lastModified: number
// }

export async function fetchProjectFile(projectId: string): Promise<File | null> {
    const user = await getUser()
    if (!user) {
        throw new Error('User authentication failed')
    }
    try {
        const projectRes = await fetch(`${serverUrl}/jobs/${projectId}`, {
            headers: {
                Authorization: `Bearer ${user?.accessToken}`,
                'Content-Type': 'application/json'
            }
        })
        const project = await projectRes.json();
        const fileId = project.data.reference_file_id
        const fileRes = await fetch(`${serverUrl}/files/download/${fileId}`, {
            headers: {
                Authorization: `Bearer ${user?.accessToken}`,
                'Content-Type': 'application/json'
            }
        })
        const fileBlob = await fileRes.blob()
        return new File([fileBlob], project.data.file_name, {type: fileBlob.type});
    } catch (error) {
        console.error('Error fetching project file:', error)
        return null;
    }
} 