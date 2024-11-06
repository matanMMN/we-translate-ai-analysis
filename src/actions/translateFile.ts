'use server'

import {revalidatePath} from 'next/cache'
import {createHash} from 'crypto'
import path from 'path'
import fs from 'fs/promises'
import {srcFile} from './srcFile'

interface TranslationResponse {
    success: boolean
    docxHash?: string
    commentsHash?: string
    fileId?: string
    mockContent?: string
    error?: string
}

export async function translateFile(formData: FormData): Promise<TranslationResponse> {
    const file = formData.get('file') as File
    const targetLanguage = formData.get('targetLanguage') as string
    const projectId = formData.get('projectId') as string

    if (!file || !targetLanguage || !projectId) {
        return {success: false, error: 'Missing required fields'}
    }

    try {
        // Mock translation delay
        await new Promise(resolve => setTimeout(resolve, 2000))
        if (process.env.NODE_ENV === 'development') {
            // Development: Use mock file
            const mockFile = await srcFile()

            // Create hash of the mock translated file
            const newDocxHash = createHash('md5').update(mockFile.content).digest('hex')

            // Mock empty comments for new file
            const emptyComments: any[] = []
            const commentsString = JSON.stringify(emptyComments)
            const newCommentsHash = createHash('md5').update(commentsString).digest('hex')

            // Generate a unique file ID that includes project reference
            const mockFileId = `${projectId}-translated-${Date.now()}-${newDocxHash.slice(0, 8)}`

            // Save file to mock storage
            const uploadsDir = path.join(process.cwd(), 'public', 'uploads', projectId)
            await fs.mkdir(uploadsDir, {recursive: true})
            await fs.writeFile(path.join(uploadsDir, 'document.docx'), Buffer.from(mockFile.content, 'base64'))
            await fs.writeFile(path.join(uploadsDir, 'comments.json'), commentsString)

            // Revalidate relevant paths
            revalidatePath(`/${projectId}/editor`)
            revalidatePath(`/${projectId}/translate-file`)
            return {
                success: true,
                docxHash: newDocxHash,
                commentsHash: newCommentsHash,
                fileId: mockFileId,
                mockContent: mockFile.content
            }
        } else {
            // Production: Real translation logic
            const arrayBuffer = await file.arrayBuffer()
            const buffer = Buffer.from(arrayBuffer)

            // Create hash of the translated file
            const newDocxHash = createHash('md5').update(buffer).digest('hex')

            // Mock empty comments for new file
            const emptyComments: any[] = []
            const commentsString = JSON.stringify(emptyComments)
            const newCommentsHash = createHash('md5').update(commentsString).digest('hex')

            // TODO: Send to actual translation service
            // const translatedFile = await translateFileService(buffer, targetLanguage)

            // TODO: Save to actual storage service
            // const fileId = await storageService.saveFile(translatedFile)

            const fileId = `${projectId}-translated-${Date.now()}-${newDocxHash.slice(0, 8)}`

            return {
                success: true,
                docxHash: newDocxHash,
                commentsHash: newCommentsHash,
                fileId: fileId
            }
        }



    } catch (error) {
        console.error('Translation error:', error)
        return {
            success: false,
            error: error instanceof Error ? error.message : 'Translation failed'
        }
    }
} 