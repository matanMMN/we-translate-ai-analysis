import { toast } from 'sonner';
import store from '@/store/store';
import { updateFileMetadata } from '@/store/slices/projectSlice';

interface TranslateOptions {
    text: string;
    sourceLang: string;
    targetLang: string;
    projectId: string;
}

interface TranslationResponse {
    translatedText: string;
    fileId?: string;
    docxHash?: string;
    commentsHash?: string;
}

export async function translateText({
    text,
    sourceLang,
    targetLang,
    projectId
}: TranslateOptions): Promise<TranslationResponse> {
    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text,
                sourceLang,
                targetLang,
                projectId
            })
        });

        if (!response.ok) {
            throw new Error('Translation failed');
        }

        const result = await response.json();

        // If we get file metadata from the translation, update the project state
        if (result.fileId && result.docxHash) {
            store.dispatch(updateFileMetadata({
                docxHash: result.docxHash,
                commentsHash: result.commentsHash || null,
                lastModified: Date.now()
            }));
        }

        return result;
    } catch (error) {
        toast.error('Translation failed. Please try again.');
        throw error;
    }
} 