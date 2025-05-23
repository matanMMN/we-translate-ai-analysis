'use client'

import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import {ScrollArea} from "@/components/ui/scroll-area";
import {GlossaryEntry} from "@/services/glossaryService";
import LoadingSpinner from "@/components/LoadingSpinner";

interface GlossaryListProps {
    entries: GlossaryEntry[];
    isLoading: boolean;
    sourceLang: string;
}

export function GlossaryList({entries, isLoading, sourceLang}: GlossaryListProps) {
    if (isLoading) {
        return <div className="flex justify-center p-4"><LoadingSpinner/></div>;
    }
    console.log(sourceLang)
    return (
        <ScrollArea className="h-[200px] rounded-md border">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead className="text-center">Source Text</TableHead>
                        <TableHead className="text-center">Target Text</TableHead>
                        {/*<TableHead>Date Added</TableHead>*/}
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {entries.map((entry) => (
                        <TableRow key={entry.sourceText}>
                            <TableCell className="text-center">
                                {/*<TableCell className={sourceLang === 'he' ? 'text-right' : 'text-left'}>*/}
                                {entry.sourceText}
                            </TableCell>
                            <TableCell className="text-center">
                                {entry.targetText}
                            </TableCell>
                            {/*<TableCell>*/}
                            {/*    {new Date(entry.createdAt).toLocaleDateString()}*/}
                            {/*</TableCell>*/}
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </ScrollArea>
    );
} 