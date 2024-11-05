"use server"

import fs from 'fs/promises'
import path from 'path'
import crypto from 'crypto'

interface SaveResult {
    success: boolean;
    message: string;
    docxHash?: string;
    commentsHash?: string;
}

export const srcFile = async (fileName="src.txt") => {
    const fileExt = path.extname(fileName).toLowerCase();
    const filePath = path.join(process.cwd(), 'src', 'assets', fileName);

    // Read file content
    const fileBuffer = await fs.readFile(filePath);
    const base64Content = fileBuffer.toString('base64');

    // Determine MIME type
    const mimeTypes = {
        '.txt': 'text/plain',
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    };

    return {
        content: base64Content,
        name: fileName,
        type: mimeTypes[fileExt as keyof typeof mimeTypes] || 'application/octet-stream',
        lastModified: new Date().getTime()
    };
}


export async function handleEditorChanges(
    blob: Blob,
    comments: any,
    prevDocxHash?: string | null,
    prevCommentsHash?: string | null
): Promise<SaveResult> {
    try {
        const arrayBuffer = await blob.arrayBuffer()
        const buffer = Buffer.from(arrayBuffer)

        // Generate hashes for the current document and comments
        const docxHash = crypto.createHash('md5').update(buffer).digest('hex')
        const commentsHash = crypto.createHash('md5').update(JSON.stringify(comments)).digest('hex')

        // Check if there are any changes
        if (docxHash === prevDocxHash && commentsHash === prevCommentsHash) {
            return {success: true, message: 'No changes detected', docxHash, commentsHash}
        }

        // const stringifiedComments = comments.map((comment: any) => {
        //     console.log(JSON.stringify(comment.replies))
        //     comment.replies = JSON.parse(JSON.stringify(comment.replies))
        // })
        // console.log(stringifiedComments)
        // console.log(JSON.stringify(stringifiedComments))
        // Save the document as a .docx file if changed
        if (docxHash !== prevDocxHash) {
            const docxPath = path.join(process.cwd(), 'public', 'uploads', 'document.docx')
            await fs.writeFile(docxPath, buffer)
        }
        // console.log(comments[0].replies.map(r => r()))
        // Save the comments as a .json file if changed
        if (commentsHash !== prevCommentsHash) {
            const commentsPath = path.join(process.cwd(), 'public', 'uploads', 'comments.json')
            await fs.writeFile(commentsPath, JSON.stringify(comments, null, 2))
        }

        return {
            success: true,
            message: 'Document and/or comments updated successfully',
            docxHash,
            commentsHash
        }

    } catch (error) {
        console.error('Error saving document and comments:', error)
        return {success: false, message: 'Failed to save document and comments'}
    }
}

