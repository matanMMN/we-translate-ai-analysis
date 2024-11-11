'use client'

import {DocumentEditorContainerComponent} from '@syncfusion/ej2-react-documenteditor';
import {RefObject} from 'react';
import {Session} from 'next-auth';
import {TitleBar} from '../TitleBar';
import {containsRTL} from '@/lib/utils/textUtils';
import {createSfdtContent} from '@/lib/utils/documentUtils';
import * as defaultData from '@/app/(content)/[projectId]/editor/data-default.json';
import store from '@/store/store';
import {selectProjectFiles, selectCurrentFile} from '@/store/slices/projectSlice';


export const handleFileLoad = async (
    container: RefObject<DocumentEditorContainerComponent>,
    userSession: Session | null,
    projectId: string,
    headerTitle: string,
    titleBar: TitleBar
) => {
    if (!container.current) return;

    // Set current user
    container.current.documentEditor.currentUser =
        `${userSession?.userData?.first_name} ${userSession?.userData?.last_name}`;

    try {
        const state = store.getState();
        const projectFiles = selectProjectFiles(state);
        const currentFile = selectCurrentFile(state);

        // Check localStorage first
        const savedContent = localStorage.getItem(`editorContent-${projectId}`);
        const lastSaveTime = localStorage.getItem(`lastSaveTime-${projectId}`);

        // If we have a lastModified timestamp from the backend/translation
        if (currentFile.lastModified) {
            // Check if localStorage is newer than our last known modification
            if (savedContent && lastSaveTime && parseInt(lastSaveTime) > currentFile.lastModified) {
                console.log('Using newer localStorage content');
                container.current.documentEditor.open(savedContent);
                return;
            }
            console.log(projectId, projectFiles)
            // If localStorage is older or doesn't exist, try to fetch from backend
            if (projectId && projectFiles.srcFileId) {
                try {
                    console.log('Fetching newer content from backend');
                    // const res = await fetchProjectFile(projectId, projectFiles.srcFileId);
                    const res = {blob: currentFile.blob, type: currentFile.type}
                    console.log(res)
                    if (res?.type && res.blob) {
                        // const blob = base64ToBlob(fileData.content, fileData.type);
                        await loadFileContent(container, res.blob, res.type);
                        return;
                    }
                } catch (error) {
                    console.error('Error fetching file:', error);
                }
            }
        } else if (savedContent) {
            // If we don't have a lastModified timestamp but have localStorage content
            console.log('Using localStorage content (no lastModified timestamp)');
            container.current.documentEditor.open(savedContent);
            return;
        }

        // Fallback to default content
        console.log('Using default content');
        container.current.documentEditor.open(JSON.stringify(defaultData));

        // Set document properties
        container.current.documentEditor.documentName = headerTitle;
        container.current.documentEditorSettings.showRuler = true;
        titleBar.updateDocumentTitle();

        // Set document change handler
        container.current.documentChange = () => {
            titleBar.updateDocumentTitle();
            container.current?.documentEditor.focusIn();
        };

    } catch (error) {
        console.error('Error loading file:', error);
        container.current.documentEditor.open(JSON.stringify(defaultData));
    }
};

async function loadFileContent(
    container: RefObject<DocumentEditorContainerComponent>,
    fileBlob: Blob,
    fileType: string
) {
    if (!container.current) return;
    console.log(fileType)
    switch (fileType) {
        case 'application/pdf':
            await handlePdfContent(container, fileBlob);
            break;
        case 'text/plain':
            await handleTextContent(container, fileBlob);
            break;
        default:
            await handleDocxContent(container, fileBlob);
    }
}

async function handlePdfContent(
    container: RefObject<DocumentEditorContainerComponent>,
    fileBlob: Blob
) {
    container.current?.documentEditor.open(`data:application/pdf;base64,${fileBlob}`);
    //
    // const pdfData = await fileBlob.arrayBuffer();
    // const pdfjsLib = await import('pdfjs-dist');
    // pdfjsLib.GlobalWorkerOptions.workerSrc =
    //     `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;
    //
    // const pdf = await pdfjsLib.getDocument({data: pdfData}).promise;
    // let textContent = '';
    //
    // for (let i = 1; i <= pdf.numPages; i++) {
    //     const page = await pdf.getPage(i);
    //     const text = await page.getTextContent();
    //     textContent += text.items
    //         .map((item: any) => item.str)
    //         .join(' ') + '\n';
    // }
    //
    // const sfdtContent = createSfdtContent(textContent);
    // container.current?.documentEditor.open(JSON.stringify(sfdtContent));
}

async function handleTextContent(
    container: RefObject<DocumentEditorContainerComponent>,
    fileBlob: Blob
) {
    const text = await fileBlob.text();
    console.log(text)
    const isRTL = containsRTL(text);
    const sfdtContent = createSfdtContent(text);
    container.current?.documentEditor.open(JSON.stringify(sfdtContent));

    if (isRTL && container.current) {

        if (!container.current) return;

        container.current.documentEditor.selection.selectAll();
        container.current.documentEditor.selection.paragraphFormat.textAlignment = 'Right';
        container.current.documentEditor.selection.characterFormat.bidi = true;
        container.current.documentEditor.selection.paragraphFormat.bidi = true;
        container.current.documentEditor.selection.sectionFormat.bidi = true;
        container.current.documentEditor.selection.moveToLineStart();

    }
}

async function handleDocxContent(
    container: RefObject<DocumentEditorContainerComponent>,
    fileBlob: Blob
) {
    container.current?.documentEditor.open(fileBlob);

}

// Helper function to convert base64 to Blob
// function base64ToBlob(base64: string, type: string): Blob {
//     const binaryString = window.atob(base64);
//     const bytes = new Uint8Array(binaryString.length);
//     for (let i = 0; i < binaryString.length; i++) {
//         bytes[i] = binaryString.charCodeAt(i);
//     }
//     return new Blob([bytes], {type});
// }