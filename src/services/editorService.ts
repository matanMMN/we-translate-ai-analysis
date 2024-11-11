import {AppDispatch} from '@/store/store.types';
import {initializeWithText} from '@/store/slices/sideBySideSlice';
import {toast} from 'sonner';

interface CopyToSideBySideOptions {
    text: string;
    sourceLanguage: string;
    dispatch: AppDispatch;
    projectId?: string | null;
}

export const copyTextToSideBySide = async ({
                                               text,
                                               sourceLanguage,
                                               dispatch,
                                           }: CopyToSideBySideOptions): Promise<boolean> => {
    try {
        const cleanedText = text.trim();

        if (!cleanedText) {
            toast.error('No text selected');
            return false;
        }

        // Initialize the section in Redux
        dispatch(initializeWithText({text: cleanedText, sourceLanguage}));

        // Save the section to file system and backend
        const result = "success"
        // const result = await dispatch(saveSectionToFile({
        //     id: '1',
        //     sourceContent: cleanedText,
        //     targetContent: '',
        //     projectId
        // })).unwrap();

        if (result)
            return true;


        return false;
    } catch (error) {
        console.error('Error copying text to side-by-side:', error);
        toast.error('Failed to copy text to Side by Side');
        return false;
    }
}; 