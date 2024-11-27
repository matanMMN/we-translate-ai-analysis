import {DocumentEditorContainerComponent} from '@syncfusion/ej2-react-documenteditor';
import {RefObject} from 'react';
import {MenuItemModel} from '@syncfusion/ej2-navigations';
import {AppDispatch} from '@/store/store.types';
// import {copyTextToSideBySide} from '@/services/editorService';
import {toast} from 'sonner';

interface SetupContextMenuProps {
    container: RefObject<DocumentEditorContainerComponent>;
    dispatch: AppDispatch;
    navigate: (path: string) => void;
    projectId: string | null
    sourceLanguage?: string;
}

export const setupContextMenu = ({
                                     container,
                                     // dispatch,
                                     // navigate,
                                     projectId,
                                     // sourceLanguage
                                 }: SetupContextMenuProps) => {
    if (!container.current) return;

    const menuItems: MenuItemModel[] = [
        {
            text: 'Search In Google',
            id: 'search_in_google',
            iconCss: 'e-icons e-de-ctnr-find',
        },
        // {
        //     text: `Copy to 'Side by side'`,
        //     id: 'copy_to_side',
        //     iconCss: 'e-icons e-copy',
        // },
    ];

    container.current.documentEditor.contextMenu.addCustomMenu(menuItems, false);

    container.current.documentEditor.customContextMenuSelect = async (args: { id: string }) => {
        if (!container.current) return;

        if (!projectId) {
            toast.error('Project not found');
            return;
        }
        const id: string = container.current.documentEditor.element.id;
        const selectedText = container.current.documentEditor.selection.text;

        switch (args.id) {
            case `${id}search_in_google`:
                if (!container.current.documentEditor.selection.isEmpty && /\S/.test(selectedText)) {
                    window.open(`http://google.com/search?q=${selectedText}`);
                }
                break;
            // case `${id}copy_to_side`:
            //     if (!container.current.documentEditor.selection.isEmpty && /\S/.test(selectedText)) {
            //         try {
            //             // Trigger auto-save before navigation
            //             await container.current.documentEditor.saveAsBlob("Docx");
            //
            //             // Copy the selected text to side-by-side
            //             const success = await copyTextToSideBySide({
            //                 text: selectedText,
            //                 sourceLanguage,
            //                 dispatch,
            //                 projectId
            //             });
            //             if (success) {
            //                 toast.success('Text copied to Side by Side');
            //                 // Navigate to side-by-side page
            //                 navigate('side-by-side');
            //             } else {
            //                 toast.error('Failed to copy text');
            //             }
            //         } catch (error) {
            //             console.error('Error in copy to side-by-side:', error);
            //             toast.error('Failed to copy text');
            //         }
            //     } else {
            //         toast.error('Please select some text first');
            //     }
            //     break;
        }
    };
};