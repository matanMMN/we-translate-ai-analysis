'use server'

import store from "@/store/store"
//
// interface ProjectFileResponse {
//     content: string
//     type: string
//     lastModified: number
// }

export async function fetchProjectFile(projectId: string, fileId: string): Promise<{
    blob: Blob | null,
    type: string | null
} | null> {
    try {
        // In development, read from local file system
        // if (process.env.NODE_ENV === 'development') {
            console.log(projectId, fileId)
            const state = store.getState()
            const currentFile = state.project.currentFile
            console.log(currentFile)
            return {blob: currentFile.blob!, type: currentFile.type!}
            // const filePath = path.join(process.cwd(), 'public', 'uploads', projectId, 'document.docx')
            // const fileBuffer = await fs.readFile(filePath)
            //
            // return {
            //     content: fileBuffer.toString('base64'),
            //     type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            //     lastModified: (await fs.stat(filePath)).mtimeMs
            // }
        // }
        //
        // // TODO: In production, fetch from actual storage using fileId
        // return null
    } catch (error) {
        console.error('Error fetching project file:', error)
        return null
    }
} 