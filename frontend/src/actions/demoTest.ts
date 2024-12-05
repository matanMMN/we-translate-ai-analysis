"use server"

import fs from "fs/promises"
import path from 'path'
import crypto from 'crypto'


export const srcFile = async (fileName="eng.docx") => {
    const fileExt = path.extname(fileName).toLocaleLowerCase();
    const filePath = path.join(process.cwd(), 'src', 'assets', fileName);

    const fileBuffer = await fs.readFile(filePath)
    const base64Content = fileBuffer.toString('base64')

    const mimeType = 'application/vnd.openxmlformats-officialdocument.wordprocessingml.document'

    return {
        content: base64Content,
        name: fileName,
        type: mimeType,
        lastModified: new Date().getTime()
    }
}