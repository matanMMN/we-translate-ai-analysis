import {toast} from 'sonner';
import {serverUrl} from "@/lib/functions";
import {Session} from "next-auth";
import {Project} from "@/lib/userData";

export interface GlossaryEntry {
    sourceText: string;
    targetText: string;
    sourceLang?: string;
    targetLang?: string;
    project?: Project | null;
    session?: Session | null;
    projectId?: string | null;
}

export async function addGlossaryEntry(entry: GlossaryEntry) {

    if (!entry.project)
        throw new Error('Project data is missing');
    if (!entry.session)
        throw new Error('Session data is missing');
    console.log(entry)
    console.log(`${serverUrl}/jobs/${entry.projectId}`)
    const oldGlossaries = entry?.project?.data?.glossaries
    console.log("oldGlossaries: ", oldGlossaries)
    const response = await fetch(`${serverUrl}/jobs/${entry.projectId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${entry?.session.accessToken}`
        },
        body: JSON.stringify({
            data: {
                ...entry?.project?.data,
                glossaries: [
                    ...(oldGlossaries ?? []),
                    {
                        sourceText: entry.sourceText,
                        targetText: entry.targetText,
                        sourceLang: entry.sourceLang,
                        targetLang: entry.targetLang,
                    }
                ]
            }
        })
    });

    console.log("response:", response)
    if (!response.ok) {
        throw new Error('Failed to add glossary entry');
    }
    const data = await response.json();
    console.log(response, data)
    toast.success('Glossary entry added successfully!');
    // return await response.json();
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