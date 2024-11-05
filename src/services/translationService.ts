import { toast } from 'sonner';

interface TranslateOptions {
    text: string;
    sourceLang: string;
    targetLang: string;
    projectId: string;
}

export async function translateText({
    text,
    sourceLang,
    targetLang,
    projectId
}: TranslateOptions) {
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

        return await response.json();
    } catch (error) {
        toast.error('Translation failed. Please try again.');
        throw error;
    }
} 