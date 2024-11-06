'use server'

import path from 'path'
import fs from 'fs/promises'

interface ProjectFileResponse {
    content: string
    type: string
    lastModified: number
}

export async function fetchProjectFile(projectId: string, fileId: string): Promise<ProjectFileResponse | null> {
    try {
        // In development, read from local file system
        if (process.env.NODE_ENV === 'development') {
            const filePath = path.join(process.cwd(), 'public', 'uploads', projectId, 'document.docx')
            const fileBuffer = await fs.readFile(filePath)
            
            return {
                content: fileBuffer.toString('base64'),
                type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                lastModified: (await fs.stat(filePath)).mtimeMs
            }
        }

        // TODO: In production, fetch from actual storage using fileId
        return null
    } catch (error) {
        console.error('Error fetching project file:', error)
        return null
    }
} 