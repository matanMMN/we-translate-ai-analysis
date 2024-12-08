'use server'
import { serverUrl } from "@/lib/functions";
import { getUser } from "@/lib/AuthGuard";
//
// interface ProjectFileResponse {
//     content: string
//     type: string
//     lastModified: number
// }


export async function fetchProjectRefOrSrc(projectId: string, fileType: string): Promise<File | null> {
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
        let fileId: string

        switch (fileType) {
            case 'reference':
                fileId = project.data.reference_file_id
                break;
            case 'source':
                fileId = project.data.source_file_id
                break;
            default:
                throw new Error('Invalid file type')
        }

        if (!fileId) {
            return null;
        }
        const fileRes = await fetch(`${serverUrl}/files/download/${fileId}`, {
            headers: {
                Authorization: `Bearer ${user?.accessToken}`,
                'Content-Type': 'application/json'
            }
        })
        const fileBlob = await fileRes.blob()
        return new File([fileBlob], project.data.file_name, { type: fileBlob.type });
    } catch (error) {
        console.error('Error fetching project file:', error)
        return null;
    }
}


export async function fetchProjectFile(projectId: string) {
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
        if (!project?.data.target_file_id)
            return null;
        const fileRes = await fetch(`${serverUrl}/files/download/${project.data.target_file_id}`, {
            headers: {
                Authorization: `Bearer ${user?.accessToken}`,
                'Content-Type': 'application/json'
            }
        })


        const arrayBuffer = await fileRes.arrayBuffer();
        const encodedString = Buffer.from(arrayBuffer).toString('base64');
        return {
            blob: encodedString,
            type: "docx"
        }
    } catch (error) {
        console.error('Error fetching project file:', error)
        return null;
    }
} 