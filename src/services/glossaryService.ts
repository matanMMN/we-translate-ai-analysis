import { toast } from 'sonner';

export interface GlossaryEntry {
    sourceText: string;
    targetText: string;
    sourceLang: string;
    targetLang: string;
}

export async function addGlossaryEntry(entry: GlossaryEntry) {
    try {
        const response = await fetch('/api/glossary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(entry)
        });

        if (!response.ok) {
            throw new Error('Failed to add glossary entry');
        }

        toast.success('Glossary entry added successfully!');
        return await response.json();
    } catch (error) {
        toast.error('Failed to add glossary entry');
        throw error;
    }
} 