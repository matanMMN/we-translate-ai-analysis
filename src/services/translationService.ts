import {toast} from 'sonner';
// import store from '@/store/store';
// import {updateFileMetadata} from '@/store/slices/projectSlice';
// import {serverUrl} from "@/lib/functions";
import {Session} from "next-auth";

interface TranslateOptions {
    text: string;
    sourceLang: string;
    targetLang?: string;
    projectId: string;
    userSession: Session | null
}

interface TranslationResponse {
    translatedText: string;
    fileId?: string;
    docxHash?: string;
    commentsHash?: string;
}

export async function translateText({
                                        // text,
                                        // sourceLang,
                                        // targetLang,
                                        // projectId,
                                        userSession
                                    }: TranslateOptions): Promise<TranslationResponse> {

    if (!userSession) {
        throw new Error('User authentication failed');
    }

    await new Promise(resolve => setTimeout(resolve, 1000));
    try {
        // const response = await fetch(`${serverUrl}/text`, {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //         'Authorization': `Bearer ${userSession.accessToken}`
        //     },
        //     body: JSON.stringify({
        //         source_language: sourceLang,
        //         target_language: targetLang,
        //         translation_job_id: projectId,
        //         input_text: text
        //     })
        // });
        //
        // if (!response.ok) {
        //     throw new Error('Translation failed');
        // }

        // const output = await response.json();
        const output = {
            translatedText: 'This is a test translation'
        }
        // If we get file metadata from the translation, update the project state
        // if (result.fileId && result.docxHash) {
        //     store.dispatch(updateFileMetadata({
        //         docxHash: result.docxHash,
        //         commentsHash: result.commentsHash || null,
        //         lastModified: Date.now()
        //     }));
        // }

        return output;
    } catch (error) {
        toast.error('Translation failed. Please try again.');
        throw error;
    }
} 