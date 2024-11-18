'use server'

import {createHash} from 'crypto';
import path from "path";
import fs from "fs/promises";
import {getUser} from "@/lib/AuthGuard";

interface EditorChangesResult {
    success: boolean;
    docxHash?: string;
    commentsHash?: string;
    error?: string;
}


export const handleEditorChanges = async (
    blob: Blob,
    comments: string[],
    currentDocxHash: string | null,
    currentCommentsHash: string | null,
): Promise<EditorChangesResult> => {
    try {

        const session = await getUser()
        if (!session) {
            return {success: false, error: 'Not authenticated'}
        }

        // Convert blob to array buffer
        const arrayBuffer = await blob.arrayBuffer();
        const buffer = Buffer.from(arrayBuffer);

        // Create hash of the docx content
        const newDocxHash = createHash('md5').update(buffer).digest('hex');

        // Create hash of the comments
        const commentsString = JSON.stringify(comments);
        const newCommentsHash = createHash('md5').update(commentsString).digest('hex');

        // If nothing has changed, return early
        if (newDocxHash === currentDocxHash && newCommentsHash === currentCommentsHash) {
            return {success: true};
        }

        // Here you would typically send the changes to your backend
        if (newDocxHash !== currentDocxHash) {
            const docxPath = path.join(process.cwd(), 'public', 'uploads', 'document.docx')
            await fs.writeFile(docxPath, buffer)
            try {
                const formData = new FormData();
                const file = new File([buffer], 'document.docx', {type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'});
                formData.append('file', file)

                // const res = await fetch('', {
                //     headers: {
                //         'Authorization': `Bearer ${session?.accessToken}`,
                //     },
                //     method: 'PUT',
                //     body: formData
                // })
                // const isUploaded = await res.json()
                // console.log(isUploaded)
            } catch (e) {
                console.error(e)
            }
        }


        // console.log(comments[0].replies.map(r => r()))
        // Save the comments as a .json file if changed
        if (newCommentsHash !== currentCommentsHash) {
            const commentsPath = path.join(process.cwd(), 'public', 'uploads', 'comments.json')
            await fs.writeFile(commentsPath, JSON.stringify(comments, null, 2))
        }
        // For now, we'll just return the new hashes
        return {
            success: true,
            docxHash: newDocxHash,
            commentsHash: newCommentsHash
        };

    } catch (error) {
        console.error('Error handling editor changes:', error);
        return {
            success: false,
            error: 'Failed to process editor changes'
        };
    }
}; 