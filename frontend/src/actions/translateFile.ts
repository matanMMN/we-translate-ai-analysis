'use server'

import {revalidatePath} from 'next/cache'
import {Session} from "next-auth";
import path from "path";
import {serverUrl} from "@/lib/functions";
import axios from 'axios';

interface TranslationResponse {
    success: boolean
    docxHash?: string
    commentsHash?: string
    fileId?: string
    mockBlob?: Blob | string,
    blobType?: string,
    error?: string
}

//
// interface DocxContent {
//     text: string;
//     documentXml: string;
// }

// async function extractDocxContentPreservingStructure(buffer: Buffer): Promise<DocxContent> {
//     // Load the DOCX as a ZIP file
//     const zip = new JSZip();
//     await zip.loadAsync(buffer);
//
//     // Get the main document XML
//     const documentXml = await zip.file('word/document.xml')?.async('text');
//     if (!documentXml) {
//         throw new Error('Could not find document.xml in DOCX file');
//     }
//
//     // Parse the XML
//     const parser = new DOMParser();
//     const doc = parser.parseFromString(documentXml, 'text/xml');
//
//     // Extract only text content while preserving XML structure
//     const textNodes: string[] = [];
//     const wElements = doc.getElementsByTagName('w:t');
//     for (let i = 0; i < wElements.length; i++) {
//         const node = wElements[i];
//         textNodes.push(node.textContent || '');
//     }
//
//     return {
//         text: textNodes.join(' '),
//         documentXml: documentXml
//     };
// }

// async function injectTranslatedText(originalXml: string, translatedText: string): Promise<string> {
//     const parser = new DOMParser();
//     const serializer = new XMLSerializer();
//     const doc = parser.parseFromString(originalXml, 'text/xml');
//
//     // Split translated text into chunks
//     const translatedChunks = translatedText.split('\n').filter(chunk => chunk.trim());
//     let chunkIndex = 0;
//
//     // Replace text content while preserving structure
//     const wElements = doc.getElementsByTagName('w:t');
//     for (let i = 0; i < wElements.length; i++) {
//         const node = wElements[i];
//         if (node.textContent?.trim()) {
//             node.textContent = translatedChunks[chunkIndex] || '';
//             chunkIndex++;
//         }
//     }
//
//     return serializer.serializeToString(doc);
// }

// async function createDocxWithPreservedStructure(
//     buffer: Buffer,
//     translatedText: string
// ): Promise<Buffer> {
//     const zip = new JSZip();
//
//     // Load original DOCX
//     await zip.loadAsync(buffer);
//
//     // Get and modify document.xml
//     const documentXml = await zip.file('word/document.xml')?.async('text');
//     if (!documentXml) {
//         throw new Error('Could not find document.xml in DOCX file');
//     }
//
//     // Inject translated text while preserving structure
//     const modifiedXml = await injectTranslatedText(documentXml, translatedText);
//
//     // Replace document.xml in the ZIP
//     zip.file('word/document.xml', modifiedXml);
//
//     // Generate new DOCX buffer
//     return await zip.generateAsync({type: 'nodebuffer'});
// }
//
// async function createNewDocx(translatedText: string): Promise<Buffer> {
//     // Split the text into paragraphs
//     const paragraphs = translatedText.split('\n').filter(p => p.trim());
//
//     // Create a new document
//     const doc = new Document({
//         sections: [{
//             properties: {},
//             children: paragraphs.map(text =>
//                 new Paragraph({
//                     children: [
//                         new TextRun({
//                             text: text,
//                         }),
//                     ],
//                 })
//             ),
//         }],
//     });
//
//     // Generate buffer
//     return await Packer.toBuffer(doc);
// }


const determineType = (fileExt: string) => {
    // Determine MIME type

    const mimeTypes: Record<string, string> = {
        '.txt': 'text/plain',
        '.pdf': 'text/plain',
        // '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }

    return mimeTypes[fileExt] || 'application/octet-stream'
}

// const decodeTxtFile = async (file: File) => {
//     const buffer = Buffer.from(await file.arrayBuffer())
//     const base64Content = buffer.toString('base64')
//     const binaryContent = atob(base64Content)
//     return new Blob([Uint8Array.from(binaryContent.split('').map(char => char.charCodeAt(0)))], {type: 'text/plain'})
// }

// const decodeDocxFile = async (file: File) => {
//     const buffer = Buffer.from(await file.arrayBuffer())
//     return buffer.toString('base64')
// }

// const decodePdfFile = async (file: File) => {
//
//     const extractor = getTextExtractor()
//     const buffer = Buffer.from(await file.arrayBuffer())
//     // const read = await readFile(buffer)
//     const text = await extractor.extractText({input: buffer, type: 'buffer'})
//     return decodeTxtFile(new File([text], 'document.txt'))
//
//     // const buffer = Buffer.from(await file.arrayBuffer())
//     // const base64Content = buffer.toString('base64')
//     // const binaryContent = atob(base64Content)
//     // return new Blob([Uint8Array.from(binaryContent.split('').map(char => char.charCodeAt(0)))], {type: 'application/pdf'})
//     // const buffer = Buffer.from(await file.arrayBuffer())
//     // return buffer.toString('base64')
// }

// Add these constants for default settings
// const DEFAULT_SETTINGS = {
//     API_KEY: process.env.ANTHROPIC_API_KEY || '',
//     MODEL: 'claude-3-opus-20240229',
//     MAX_TOKENS: 4000,
//     TEMPERATURE: 0.2
// } as const;
//
// // Create the system prompt function
// function createSystemPrompt() {
//     const SUCCESS_TAG = '[TRANSLATION_SUCCESSFUL]';
//     const FAIL_TAG = '[TRANSLATION_FAILED]';
//
//     return `
//     As a translation model specialized in Hebrew to English translation, your task is to accurately translate a specific paragraph from a CMI leaflet originally written in Hebrew into English, contained within the following tags: <heb_text> ... </heb_text>.
//
//     The translation should convey the original meaning, tone, style, and pertinent terminology while effectively communicating the leaflet's message and respecting cultural nuances and idiomatic expressions unique to the source material. It should be precise, well-structured, and coherent, capturing the essence of the original text.
//
//     The final translation should feel natural and fluent to English speakers, reading like an original English text while maintaining the integrity of the original content.
//
//     Contain the translation of the text within the following tags: <eng_text> ... </eng_text>.
//
//     Upon successful translation, please include the phrase ${SUCCESS_TAG} at the end and only at the end of your response to indicate that the task has been completed effectively.
//
//     If you fail for whatever reason, response with ${FAIL_TAG} and explain why.
//
// <!--    If the text you receive contains no Hebrew text, contains no medical/pharmacological information or could not appear in a CMI leaflet, respond with ${FAIL_TAG}.-->
//
//     Provide a response without any additional information or comments besides the previously stated phrase and annotations.
//
//     Do not translate html tags and translate the texts inside each tag while keeping their output in their corresponding position.
//   `;
// }

// async function translateWithLLM(text: string) {
//     const anthropic = new Anthropic({
//         apiKey: DEFAULT_SETTINGS.API_KEY,
//     });
//     const response: any = await anthropic.messages.create({
//         model: DEFAULT_SETTINGS.MODEL,
//         max_tokens: DEFAULT_SETTINGS.MAX_TOKENS,
//         temperature: DEFAULT_SETTINGS.TEMPERATURE,
//         system: createSystemPrompt(),
//         messages: [{
//             role: 'user',
//             content: `<heb_text>${text}</heb_text>`
//         }]
//     });
//
//     const rawText = response.content[0].text;
//     console.log("response: ", rawText)
//     if (rawText.includes('[TRANSLATION_SUCCESSFUL]')) {
//         const startTag = '<eng_text>';
//         const endTag = '</eng_text>';
//         const startIndex = rawText.indexOf(startTag) + startTag.length;
//         const endIndex = rawText.indexOf(endTag);
//         return rawText.substring(startIndex, endIndex).trim();
//     } else {
//         // throw new Error(`Translation failed. Raw output: ${rawText}`);
//         throw new Error(`Translation failed.\nMake sure the source and target languages are accurate.`);
//     }
// }

export async function translateFile(formData: FormData, detectedLanguage: string, targetLanguage: string, projectId: string, session: Session, projectData: any): Promise<TranslationResponse> {

    if (!formData || !detectedLanguage || !targetLanguage || !projectId) {
        return {success: false, error: 'Missing required fields'}
    }

    const fileCopy = formData.get('file') as File;
    const fileExt = path.extname(fileCopy.name).toLowerCase()
    const type = determineType(fileExt)

    if (fileExt !== '.docx')
        return {success: false, error: 'Only DOCX files are supported at this moment'}

    // First send file and attach it to the project
    // #1 Send file to back
    const srcFileRes = await fetch(`${serverUrl}/files/upload/`, {
        headers: {
            'Authorization': `Bearer ${session.accessToken}`,
        },
        method: 'POST',
        body: formData
    });
    const srcFileData = await srcFileRes.json();
    if (srcFileData && srcFileData.status_code !== 201)
        return {success: false, error: 'Failed to process the file'}
    console.log(projectData)

    // #2 Inject src file ID into project
    const updateProject = await fetch(`${serverUrl}/jobs/${projectId}/`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.accessToken}`,
            'accept': 'application/json'
        },
        method: 'PUT',
        body: JSON.stringify({
            source_file_id: srcFileData.data.id,
            is_translating: true,
            data: {
                ...projectData,
                sideBySideSections: [],
            }
        })
    })
    const isUpdateSuccess = await updateProject.json()


    if (isUpdateSuccess && isUpdateSuccess.status_code !== 200)
        return {success: false, error: 'Failed to process the file'}

    // #3 Ask for the translated version
    const isTranslationRes = await axios.post(`${serverUrl}/translations/file/${srcFileData.data.id}`, {
        translation_job_id: isUpdateSuccess.data.id,
        source_language: detectedLanguage,
        target_language: targetLanguage,
        target_file_format: fileExt.slice(1)
    }, {
        timeout: 600000,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.accessToken}`,
        }
    });

    const isTranslationSuccess = isTranslationRes.data;
    // console.log(isTranslationSuccess)
    if (isTranslationSuccess && isTranslationSuccess?.status_code === 422)
        return {success: false, error: 'File does not contain significant medical/pharmacological context'}

    if (isTranslationSuccess && isTranslationSuccess?.status_code !== 200)
        return {success: false, error: 'Failed to process the file'}

    // #4 Get the translated file
    const translatedFileRes = await fetch(`${serverUrl}/files/download/${isTranslationSuccess.data.id}`, {
        headers: {
            'Authorization': `Bearer ${session.accessToken}`,
        },
    })
    // console.log(translatedFileRes)
    if (!translatedFileRes)
        return {success: false, error: 'Failed to process the file'}


    // #5 Return the translated file but first let the client know that the file is done translating
    const updateIsTranslatingRes = await fetch(`${serverUrl}/jobs/${projectId}/`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.accessToken}`,
            'accept': 'application/json'
        },
        method: 'PUT',
        body: JSON.stringify({
            source_file_id: srcFileData.data.id,
            data: {
                ...projectData,
                sideBySideSections: [],
            }
        })
    })
    const isUpdateIsTranslatingSuccess = await updateIsTranslatingRes.json()
    if (isUpdateIsTranslatingSuccess && isUpdateIsTranslatingSuccess.status_code !== 200)
        return {success: false, error: 'Failed to process isTranslating change'}

    try {
        const arrayBuffer = await translatedFileRes.arrayBuffer();
        const encodedString = Buffer.from(arrayBuffer).toString('base64');


        revalidatePath(`/${projectId}/editor`);

        return {
            success: true,
            fileId: srcFileData.data.id,
            mockBlob: encodedString,
            blobType: type
        };

    } catch
        (error) {
        console.log('Translation error:', error)
        return {
            success: false,
            error: error instanceof Error ? error.message : 'Translation failed'
        }
    }
} 