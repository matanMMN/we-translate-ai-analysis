import { toast } from 'sonner';

export async function translateText(text: string, sourceLang: string, targetLang: string) {
    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text,
                sourceLang,
                targetLang
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