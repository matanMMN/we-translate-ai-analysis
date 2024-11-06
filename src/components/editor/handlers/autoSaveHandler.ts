'use client'

import { DocumentEditorContainerComponent } from '@syncfusion/ej2-react-documenteditor';
import { RefObject, MutableRefObject } from 'react';
import { handleEditorChanges } from '@/actions/EditorChanges';
import store from '@/store/store';
import { updateFileMetadata } from '@/store/slices/projectSlice';

const LOCAL_SAVE_INTERVAL = 1000;   // 1 seconds
const BACKEND_SAVE_INTERVAL = 30000; // 30 seconds

export const handleAutoSave = (
    container: RefObject<DocumentEditorContainerComponent>,
    contentChanged: MutableRefObject<boolean>,
    docxHash: string | null,
    commentsHash: string | null,
    setDocxHash: (hash: string | null) => void,
    setCommentsHash: (hash: string | null) => void
) => {

    const saveToLocalStorage = (content: string) => {
        localStorage.setItem('editorContent', content);
        localStorage.setItem('lastSaveTime', Date.now().toString());
        contentChanged.current = false;
    };

    const saveToBackend = async () => {
        if (!container.current || !contentChanged.current) return;

        try {
            const blob = await container.current.documentEditor.saveAsBlob("Docx");
            const comments = container.current.documentEditor.getComments().map(comment => ({
                ...comment,
                replies: JSON.parse(JSON.stringify(comment.replies))
            }));

            const result = await handleEditorChanges(blob, comments, docxHash, commentsHash);

            if (result.success) {
                const newMetadata = {
                    docxHash: result.docxHash || null,
                    commentsHash: result.commentsHash || null,
                    lastModified: Date.now()
                }
                
                // Update Redux state
                store.dispatch(updateFileMetadata(newMetadata))
                
                // Update local state
                if (result.docxHash) setDocxHash(result.docxHash);
                if (result.commentsHash) setCommentsHash(result.commentsHash);
                
                contentChanged.current = false;
                updateSaveIndicator();
            }
        } catch (error) {
            console.error('Backend save failed:', error);
        }
    };

    // Local storage save interval (every 3 seconds)
    const localSaveIntervalId = setInterval(() => {
        if (container.current && contentChanged.current) {
            const content = container.current.documentEditor.serialize();
            saveToLocalStorage(content);
            console.log('Saved to localStorage');
        }
    }, LOCAL_SAVE_INTERVAL);

    // Backend save interval (every 30 seconds)
    const backendSaveIntervalId = setInterval(async () => {
        if (contentChanged.current) {
            console.log('Backend save triggered');
            await saveToBackend();
        }
    }, BACKEND_SAVE_INTERVAL);

    // Set up the content change handler
    if (container.current) {
        container.current.contentChange = () => {
            contentChanged.current = true;
        };

        // Also set up the documentChange event as backup
        container.current.documentEditor.documentChange = () => {
            contentChanged.current = true;
        };
    }

    // Cleanup function
    return () => {
        clearInterval(localSaveIntervalId);
        clearInterval(backendSaveIntervalId);
    };
};

function updateSaveIndicator() {
    const date = new Date();
    const time = `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
    const span = document.createElement("span");
    span.innerHTML = `Auto saved at <b>${time}</b><hr>`;
} 