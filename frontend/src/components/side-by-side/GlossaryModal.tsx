'use client'

import {useCallback, useState} from 'react';
import {Dialog, DialogContent, DialogHeader, DialogTitle} from "@/components/ui/dialog";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";
import {Label} from "@/components/ui/label";
import {addGlossaryEntry, type GlossaryEntry} from '@/services/glossaryService';
import {toast} from 'sonner';
import {useEffect} from 'react';
import {GlossaryList} from './GlossaryList';
import {useAppSelector} from "@/hooks/useAppSelector";
import {selectSession} from "@/store/slices/sessionSlice";

interface GlossaryModalProps {
    open: boolean;
    onOpenChangeAction: (open: boolean) => void;
    sourceLang: string;
    targetLang: string;
    projectId: string | null;
}

export function GlossaryModal({
                                  open,
                                  onOpenChangeAction,
                                  sourceLang,
                                  targetLang,
                                  projectId
                              }: GlossaryModalProps) {
    const [sourceText, setSourceText] = useState('');
    const [targetText, setTargetText] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [entries, setEntries] = useState<GlossaryEntry[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const {project, userSession} = useAppSelector(selectSession)

    console.log("glossaries: ", entries, project)
    const loadGlossaryEntries = useCallback(async () => {
        try {
            if (projectId) {
                const data = project?.data?.glossaries
                // const data = await fetchGlossaryEntries(projectId);
                setEntries(data);
            } else {
                throw new Error("Project ID is missing");
            }
        } catch (error) {
            console.error('Failed to load glossary entries:', error);
        } finally {
            setIsLoading(false);
        }
    }, [project?.data?.glossaries, projectId]);

    useEffect(() => {
        if (open) {
            loadGlossaryEntries();
        }
    }, [loadGlossaryEntries, open, projectId]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!sourceText || !targetText) {
            toast.error('Please fill in both fields');
            return;
        }
        setIsSubmitting(true);
        try {
            await addGlossaryEntry({
                sourceText,
                targetText,
                sourceLang,
                targetLang,
                project,
                session: userSession,
                projectId
            });

            // Refresh entries
            await loadGlossaryEntries();
            setEntries(entries => [...entries, {sourceText, targetText}]);
            // Reset form
            setSourceText('');
            setTargetText('');
        } catch (error: any) {
            toast.error('Failed to add glossary entry:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChangeAction}>
            <DialogContent className="sm:max-w-[700px]">
                <DialogHeader>
                    <DialogTitle>Glossary</DialogTitle>
                </DialogHeader>

                <div className="space-y-6">
                    {entries && !!entries.length ? <GlossaryList
                            entries={entries}
                            isLoading={isLoading}
                            sourceLang={sourceLang}
                        /> :
                        <div className="flex justify-center p-4">No glossaries added yet</div>
                    }

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="sourceText">Source Text</Label>
                            <Input
                                id="sourceText"
                                value={sourceText}
                                onChange={(e) => setSourceText(e.target.value)}
                                placeholder="Enter source text"
                                className="text-left"
                                // className={sourceLang === 'he' ? 'text-right' : 'text-left'}
                                // dir={sourceLang === 'he' ? 'rtl' : 'ltr'}
                                dir={"ltr"}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="targetText">Target Text</Label>
                            <Input
                                id="targetText"
                                value={targetText}
                                onChange={(e) => setTargetText(e.target.value)}
                                placeholder="Enter target text"
                                // className="text-right"
                                className="text-left"
                                dir={"ltr"}
                                // dir="rtl"
                            />
                        </div>
                        <div className="flex justify-end gap-2">
                            <Button
                                type="button"
                                variant="outline"
                                onClick={() => onOpenChangeAction(false)}
                            >
                                Cancel
                            </Button>
                            <Button
                                type="submit"
                                className="bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white"
                                disabled={isSubmitting}
                            >
                                {isSubmitting ? 'Adding...' : 'Add to Glossary'}
                            </Button>
                        </div>
                    </form>
                </div>
            </DialogContent>
        </Dialog>
    );
} 