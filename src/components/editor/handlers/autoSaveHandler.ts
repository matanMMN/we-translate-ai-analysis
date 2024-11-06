import {DocumentEditorContainerComponent} from '@syncfusion/ej2-react-documenteditor';
import {RefObject, MutableRefObject} from 'react';
import {handleEditorChanges} from '@/actions/EditorChanges';


export const handleAutoSave = (
    container: RefObject<DocumentEditorContainerComponent>,
    contentChanged: MutableRefObject<boolean>,
    docxHash: string | null,
    commentsHash: string | null,
    setDocxHash: (hash: string | null) => void,
    setCommentsHash: (hash: string | null) => void
) => {
    const saveChanges = async () => {
        console.log("saveChanges")
        if (contentChanged.current && container.current) {
            try {
                console.log("performing an auto save")
                const blob = await container.current.documentEditor.saveAsBlob("Docx");

                const comments = container.current.documentEditor.getComments().map(comment => ({
                    ...comment,
                    replies: JSON.parse(JSON.stringify(comment.replies))
                }));

                const result = await handleEditorChanges(blob, comments, docxHash, commentsHash);

                if (result.success) {
                    if (result.docxHash) setDocxHash(result.docxHash);
                    if (result.commentsHash) setCommentsHash(result.commentsHash);
                }

                updateSaveIndicator();
                contentChanged.current = false;

                const content = container.current.documentEditor.serialize();
                localStorage.setItem('editorContent', content);
            } catch (error) {
                console.error('Auto-save failed:', error);
            }
        }
    }
    // const debouncedSaveChanges = debounce(saveChanges, 5000);
    const intervalId = setInterval(saveChanges, 3000);
    return () => clearInterval(intervalId);
};

function updateSaveIndicator() {
    const date = new Date();
    const time = `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
    const span = document.createElement("span");
    span.innerHTML = `Auto saved at <b>${time}</b><hr>`;
} 