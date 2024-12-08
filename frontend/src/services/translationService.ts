"use server"
import {toast} from 'sonner';
// import store from '@/store/store';
// import {updateFileMetadata} from '@/store/slices/projectSlice';
import {Session} from "next-auth";
import {serverUrl} from "@/lib/functions";

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
                                        text,
                                        sourceLang,
                                        targetLang,
                                        projectId,
                                        userSession
                                    }: TranslateOptions): Promise<TranslationResponse> {

    if (!userSession) {
        throw new Error('User authentication failed');
    }


    try {
        // return {
        //     translatedText: 'This is a test translation'
        // }
        const response = await fetch(`${serverUrl}/translations/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userSession.accessToken}`
            },
            body: JSON.stringify({
                source_language: sourceLang,
                target_language: targetLang,
                translation_job_id: projectId,
                input_text: text
            })
        });

        if (!response.ok) {
            throw new Error('Translation failed');
        }

        const output = await response.json();
        return {
            translatedText: output.data.output_text
        }

    } catch (error) {
        toast.error('Translation failed. Please try again.');
        throw error;
    }
} 