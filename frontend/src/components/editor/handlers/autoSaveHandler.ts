'use client'

import { DocumentEditorContainerComponent } from '@syncfusion/ej2-react-documenteditor';
import { RefObject, useRef, useEffect } from 'react';
import { handleEditorChanges } from '@/actions/EditorChanges';
// import store from '@/store/store';
// import { updateFileMetadata } from '@/store/slices/projectSlice';
import { useSelector } from "react-redux";
import { selectSession } from "@/store/slices/sessionSlice";
import { createHash } from 'crypto';

const LOCAL_SAVE_INTERVAL = 1000;   // 1 second
const BACKEND_SAVE_INTERVAL = 30000; // 30 seconds
// const IDLE_TIMEOUT = 1500; // time of activity to be considered idle

export const useAutoSave = (
    container: RefObject<DocumentEditorContainerComponent>,
    docxHash: string | null,
    commentsHash: string | null,
    setDocxHash: (hash: string | null) => void,
    setCommentsHash: (hash: string | null) => void
) => {
    const localChanges = useRef(false);
    const backendChanges = useRef(false);
    const localSaveIntervalId = useRef<NodeJS.Timeout>();
    const backendSaveIntervalId = useRef<NodeJS.Timeout>();
    const isFirstSave = useRef(true);
    const { projectId, project } = useSelector(selectSession)

    useEffect(() => {
        const saveToLocalStorage = (content: string) => {
            const hash = createHash('md5').update(content).digest('hex');
            console.log(hash)
            if (hash !== '32d459f17c479075db3ddc7e1adc482c') {
                localStorage.setItem(`editorContent-${projectId}`, content);
                localStorage.setItem(`lastSaveTime-${projectId}`, Date.now().toString());
            }
            localChanges.current = false;
        };

        const saveToBackend = async () => {

            if (!container.current) return;

            try {
                const blob = await container.current.documentEditor.saveAsBlob("Docx");
                const comments = container.current.documentEditor.getComments().map(comment => ({
                    ...comment,
                    replies: JSON.parse(JSON.stringify(comment.replies))
                }));

                const result = await handleEditorChanges(blob, comments as unknown as string[], docxHash, commentsHash, project?.target_file_id);

                console.log(result)
                if (result.success) {
                    // const newMetadata = {
                    //     docxHash: result.docxHash || null,
                    //     commentsHash: result.commentsHash || null,
                    //     lastModified: Date.now()
                    // }

                    // store.dispatch(updateFileMetadata(newMetadata));

                    if (result.docxHash) setDocxHash(result.docxHash);
                    if (result.commentsHash) setCommentsHash(result.commentsHash);

                    backendChanges.current = false;
                    updateSaveIndicator();
                }
            } catch (error) {
                console.error('Backend save failed:', error);
            }
        };
        if (container.current) {
            const editor = container.current.documentEditor;
            // Set up all editor event handlers to mark content as changed
            container.current.contentChange = () => {
                localChanges.current = true;
                backendChanges.current = true;
            };

            editor.documentChange = () => {
                localChanges.current = true;
                backendChanges.current = true;
            };

            // Start intervals
            localSaveIntervalId.current = setInterval(async () => {

                if (container.current && localChanges.current) {
                    const content = container.current.documentEditor.serialize();
                    saveToLocalStorage(content);
                    console.log('Saved to localStorage');

                    if (isFirstSave.current) {
                        console.log('First save - triggering backend save');
                        isFirstSave.current = false;
                        await saveToBackend();
                    }
                }
            }, LOCAL_SAVE_INTERVAL);

            backendSaveIntervalId.current = setInterval(async () => {
                if (backendChanges.current) {
                    console.log('Backend save triggered');
                    await saveToBackend();
                }
            }, BACKEND_SAVE_INTERVAL);
        }

        return () => {
            if (localSaveIntervalId.current) clearInterval(localSaveIntervalId.current);
            if (backendSaveIntervalId.current) clearInterval(backendSaveIntervalId.current);
        };
    }, [container, docxHash, commentsHash, setDocxHash, setCommentsHash]);
};

function updateSaveIndicator() {
    const date = new Date();
    const time = `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
    const span = document.createElement("span");
    span.innerHTML = `Auto saved at <b>${time}</b><hr>`;
} 