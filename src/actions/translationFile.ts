'use server'

import { revalidatePath } from 'next/cache'
import { createHash } from 'crypto'
import path from 'path'
import fs from 'fs/promises'

interface TranslationResponse {
    success: boolean
    docxHash?: string
    commentsHash?: string
    fileId?: string
    error?: string
}

export async function translateFile(formData: FormData): Promise<TranslationResponse> {
    const file = formData.get('file') as File
    const targetLanguage = formData.get('targetLanguage') as string
    const projectId = formData.get('projectId') as string

    if (!file || !targetLanguage || !projectId) {
        return { success: false, error: 'Missing required fields' }
    }

    try {
        // Mock translation delay
        await new Promise(resolve => setTimeout(resolve, 2000))

        // Convert file to buffer
        const arrayBuffer = await file.arrayBuffer()
        const buffer = Buffer.from(arrayBuffer)

        // Create hash of the translated file
        const newDocxHash = createHash('md5').update(buffer).digest('hex')

        // Mock empty comments for new file
        const emptyComments: any[] = []
        const commentsString = JSON.stringify(emptyComments)
        const newCommentsHash = createHash('md5').update(commentsString).digest('hex')

        // Generate a unique file ID that includes project reference
        const mockFileId = `${projectId}-translated-${Date.now()}-${newDocxHash.slice(0, 8)}`

        // In development, save to local storage and file system
        if (process.env.NODE_ENV === 'development') {
            // Save to localStorage (this will be picked up by the client)
            const content = await file.text()
            localStorage.setItem('editorContent', content)
            localStorage.setItem('lastSaveTime', Date.now().toString())

            // Save file to mock storage
            const uploadsDir = path.join(process.cwd(), 'public', 'uploads', projectId)
            await fs.mkdir(uploadsDir, { recursive: true })
            await fs.writeFile(path.join(uploadsDir, 'document.docx'), buffer)
            await fs.writeFile(path.join(uploadsDir, 'comments.json'), commentsString)
        }

        // Revalidate relevant paths
        revalidatePath(`/project/${projectId}/editor`)
        revalidatePath(`/project/${projectId}/translate-file`)

        return {
            success: true,
            docxHash: newDocxHash,
            commentsHash: newCommentsHash,
            fileId: mockFileId
        }
    } catch (error) {
        console.error('Translation error:', error)
        return {
            success: false,
            error: error instanceof Error ? error.message : 'Translation failed'
        }
    }
}