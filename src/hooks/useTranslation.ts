import { useState } from 'react';
import { toast } from 'sonner';

export function useTranslation() {
    const [isTranslating, setIsTranslating] = useState(false);

    const translate = async (text: string, sourceLang: string, targetLang: string) => {
        setIsTranslating(true);
        try {
            // Replace with your actual translation API call
            const response = await fetch('/api/translate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, sourceLang, targetLang })
            });
            
            if (!response.ok) throw new Error('Translation failed');
            
            const data = await response.json();
            return data.translatedText;
        } catch (error) {
            toast.error('Translation failed. Please try again.');
            throw error;
        } finally {
            setIsTranslating(false);
        }
    };

    return { translate, isTranslating };
} 