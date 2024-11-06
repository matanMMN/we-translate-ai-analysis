import { toast } from 'sonner';

export interface GlossaryEntry {
    sourceText: string;
    targetText: string;
    sourceLang: string;
    targetLang: string;
    projectId: string | null;
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

export async function fetchGlossaryEntries(projectId: string) {
    try {
        const response = await fetch(`/api/glossary?projectId=${projectId}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch glossary entries');
        }

        return await response.json();
    } catch (error) {
        toast.error('Failed to fetch glossary entries');
        throw error;
    }
} 