import { useState } from 'react';
import { toast } from 'sonner';

interface GlossaryEntry {
    sourceText: string;
    targetText: string;
    sourceLang: string;
    targetLang: string;
}

export function useGlossary() {
    const [isLoading, setIsLoading] = useState(false);

    const addGlossaryEntry = async (entry: GlossaryEntry) => {
        setIsLoading(true);
        try {
            const response = await fetch('/api/glossary', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(entry)
            });

            if (!response.ok) throw new Error('Failed to add glossary entry');

            toast.success('Glossary entry added successfully!');
        } catch (error) {
            toast.error('Failed to add glossary entry');
            throw error;
        } finally {
            setIsLoading(false);
        }
    };

    return { addGlossaryEntry, isLoading };
} 