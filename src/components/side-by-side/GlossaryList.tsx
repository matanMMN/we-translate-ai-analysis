'use client'

import { useEffect, useState } from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { ScrollArea } from "@/components/ui/scroll-area";

interface GlossaryEntry {
    id: string;
    sourceText: string;
    targetText: string;
    sourceLang: string;
    targetLang: string;
    createdAt: string;
}

export function GlossaryList({ sourceLang, targetLang }: { sourceLang: string; targetLang: string }) {
    const [entries, setEntries] = useState<GlossaryEntry[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchGlossary = async () => {
            try {
                const response = await fetch(`/api/glossary?sourceLang=${sourceLang}&targetLang=${targetLang}`);
                if (!response.ok) throw new Error('Failed to fetch glossary');
                const data = await response.json();
                setEntries(data);
            } catch (error) {
                console.error('Error fetching glossary:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchGlossary();
    }, [sourceLang, targetLang]);

    if (isLoading) {
        return <div className="flex justify-center p-4">Loading...</div>;
    }

    return (
        <ScrollArea className="h-[200px] rounded-md border">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Source Text</TableHead>
                        <TableHead>Target Text</TableHead>
                        <TableHead>Date Added</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {entries.map((entry) => (
                        <TableRow key={entry.id}>
                            <TableCell className={sourceLang === 'he' ? 'text-right' : 'text-left'}>
                                {entry.sourceText}
                            </TableCell>
                            <TableCell className="text-right">
                                {entry.targetText}
                            </TableCell>
                            <TableCell>
                                {new Date(entry.createdAt).toLocaleDateString()}
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </ScrollArea>
    );
} 