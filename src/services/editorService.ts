import {AppDispatch} from '@/store/store.types';
import {initializeWithText} from '@/store/slices/sideBySideSlice';
import {toast} from 'sonner';

interface CopyToSideBySideOptions {
    text: string;
    sourceLanguage?: string;
    dispatch: AppDispatch;
    projectId: string;
}

export const copyTextToSideBySide = async ({
                                               text,
                                               sourceLanguage,
                                               dispatch,
                                               projectId
                                           }: CopyToSideBySideOptions): Promise<boolean> => {
    try {
        const cleanedText = text.trim();
        if (!cleanedText) {
            toast.error('No text selected');
            return false;
        }
        if (!projectId) {
            toast.error('Project not found');
            return false;
        }

        // Initialize the section in Redux
        dispatch(initializeWithText({text: cleanedText, sourceLanguage, projectId}));

        const result = "success"

        return !!result;


    } catch (error) {
        console.error('Error copying text to side-by-side:', error);
        toast.error('Failed to copy text to Side by Side');
        return false;
    }
}; 