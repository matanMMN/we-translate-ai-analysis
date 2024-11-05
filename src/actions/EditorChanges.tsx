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


// import type { NextApiRequest, NextApiResponse } from 'next'
// import fs from 'fs'
// import path from 'path'
// import { IncomingForm } from 'formidable'
//
// export const config = {
//     api: {
//         bodyParser: false,
//     },
// }

// export default async function handler(req: NextApiRequest, res: NextApiResponse) {
//     if (req.method !== 'POST') {
//         return res.status(405).json({ message: 'Method not allowed' })
//     }
//
//     try {
//         const form = new IncomingForm()
//         form.parse(req, async (err, fields, files) => {
//             if (err) {
//                 console.error('Error parsing form:', err)
//                 return res.status(500).json({ message: 'Error parsing form data' })
//             }
//
//             const fileName = fields.fileName as string
//             const comments = JSON.parse(fields.comments as string)
//
//             // Save docx file
//             const docxFile = files.docx as any
//             const docxPath = path.join(process.cwd(), 'public', 'uploads', `${fileName}.docx`)
//             await fs.promises.rename(docxFile.filepath, docxPath)
//
//             // Save comments as JSON
//             const commentsPath = path.join(process.cwd(), 'public', 'uploads', `${fileName}-comments.json`)
//             await fs.promises.writeFile(commentsPath, JSON.stringify(comments, null, 2))
//
//             res.status(200).json({ message: 'Document and comments saved successfully' })
//         })
//     } catch (error) {
//         console.error('Error saving document and comments:', error)
//         res.status(500).json({ message: 'Error saving document and comments' })
//     }
// }