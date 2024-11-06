'use server'

import path from "path"
import fs from "fs/promises"

interface FileResponse {
    content: string
    name: string
    type: string
    lastModified: number
}

export const srcFile = async (fileName = "src.txt"): Promise<FileResponse> => {
    const fileExt = path.extname(fileName).toLowerCase()
    const filePath = path.join(process.cwd(), 'src', 'assets', fileName)

    // Read file content
    const fileBuffer = await fs.readFile(filePath)
    const base64Content = fileBuffer.toString('base64')

    // Determine MIME type
    const mimeTypes: Record<string, string> = {
        '.txt': 'text/plain',
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }

    return {
        content: base64Content,
        name: fileName,
        type: mimeTypes[fileExt] || 'application/octet-stream',
        lastModified: new Date().getTime()
    }
} 