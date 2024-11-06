import {DocumentEditorContainerComponent} from '@syncfusion/ej2-react-documenteditor';
import {RefObject} from 'react';
import {Session} from 'next-auth';
import {TitleBar} from '../TitleBar';
import {containsRTL} from '@/lib/utils/textUtils';
import {srcFile} from '@/actions/EditorChanges';
import {createSfdtContent} from '@/lib/utils/documentUtils';
import * as defaultData from '@/app/(content)/[projectId]/editor/data-default.json';

export const handleFileLoad = async (
    container: RefObject<DocumentEditorContainerComponent>,
    userSession: Session | null,
    headerTitle: string,
    titleBar: TitleBar
) => {
    if (!container.current) return;

    // Set current user
    container.current.documentEditor.currentUser =
        `${userSession?.userData?.first_name} ${userSession?.userData?.last_name}`;

    try {
        const savedContent = localStorage.getItem('editorContent');
        if (savedContent) {
            container.current.documentEditor.open(savedContent);
        } else {
            const srcFileData = await srcFile();

            if (srcFileData) {
                const binaryContent = atob(srcFileData.content);
                const fileBlob = new Blob(
                    [Uint8Array.from(binaryContent.split('').map(char => char.charCodeAt(0)))],
                    {type: srcFileData.type}
                );

                await loadFileContent(container, fileBlob, srcFileData.type);
            } else {
                // Load default content if no file exists
                container.current.documentEditor.open(JSON.stringify(defaultData));
            }
        }

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
    const pdfData = await fileBlob.arrayBuffer();
    const pdfjsLib = await import('pdfjs-dist');
    pdfjsLib.GlobalWorkerOptions.workerSrc =
        `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

    const pdf = await pdfjsLib.getDocument({data: pdfData}).promise;
    let textContent = '';

    for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const text = await page.getTextContent();
        textContent += text.items
            .map((item: any) => item.str)
            .join(' ') + '\n';
    }

    const sfdtContent = createSfdtContent(textContent);
    container.current?.documentEditor.open(JSON.stringify(sfdtContent));
}

async function handleTextContent(
    container: RefObject<DocumentEditorContainerComponent>,
    fileBlob: Blob
) {
    const text = await fileBlob.text();
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
    const reader = new FileReader();
    reader.onload = (event) => {
        container.current?.documentEditor.open(event.target?.result as string);
    };
    reader.readAsBinaryString(fileBlob);
} 