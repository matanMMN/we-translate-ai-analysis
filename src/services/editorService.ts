import {AppDispatch} from '@/store/store.types';
import {initializeWithText, saveSectionToFile} from '@/store/slices/sideBySideSlice';
import {toast} from 'sonner';

interface CopyToSideBySideOptions {
    text: string;
    sourceLanguage: string;
    dispatch: AppDispatch;
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
        await dispatch(initializeWithText({
            text: cleanedText,
            sourceLanguage
        }));

        // Save the section to file system and backend
        const result = await dispatch(saveSectionToFile({
            id: '1',
            sourceContent: cleanedText,
            targetContent: '',
        })).unwrap();

        if (result) {
            toast.success('Text copied to Side by Side');
            return true;
        }

        return false;
    } catch (error) {
        console.error('Error copying text to side-by-side:', error);
        toast.error('Failed to copy text to Side by Side');
        return false;
    }
}; 