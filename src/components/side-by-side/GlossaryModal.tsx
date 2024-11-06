'use client'

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { addGlossaryEntry, fetchGlossaryEntries, type GlossaryEntry } from '@/services/glossaryService';
import { toast } from 'sonner';
import { useEffect } from 'react';
import { GlossaryList } from './GlossaryList';

interface GlossaryModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    sourceLang: string;
    targetLang: string;
    projectId: string | null;
}

export function GlossaryModal({ 
    open, 
    onOpenChange,
    sourceLang,
    targetLang,
    projectId
}: GlossaryModalProps) {
    const [sourceText, setSourceText] = useState('');
    const [targetText, setTargetText] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [entries, setEntries] = useState<GlossaryEntry[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (open) {
            // loadGlossaryEntries();
        }
    }, [open, projectId]);

    const loadGlossaryEntries = async () => {
        try {
            if (projectId) {
                const data = await fetchGlossaryEntries(projectId);
                setEntries(data);
            } else {
                throw new Error("Project ID is missing");
            }
        } catch (error) {
            console.error('Failed to load glossary entries:', error);
        } finally {
            setIsLoading(false);
        }
    };

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
                projectId
            });

            // Refresh entries
            await loadGlossaryEntries();

            // Reset form
            setSourceText('');
            setTargetText('');
        } catch (error) {
            console.error('Failed to add glossary entry:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[700px]">
                <DialogHeader>
                    <DialogTitle>Glossary</DialogTitle>
                </DialogHeader>
                
                <div className="space-y-6">
                    <GlossaryList 
                        entries={entries} 
                        isLoading={isLoading} 
                        sourceLang={sourceLang}
                    />
                    
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="sourceText">Source Text</Label>
                            <Input
                                id="sourceText"
                                value={sourceText}
                                onChange={(e) => setSourceText(e.target.value)}
                                placeholder="Enter source text..."
                                className={sourceLang === 'he' ? 'text-right' : 'text-left'}
                                dir={sourceLang === 'he' ? 'rtl' : 'ltr'}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="targetText">Target Text</Label>
                            <Input
                                id="targetText"
                                value={targetText}
                                onChange={(e) => setTargetText(e.target.value)}
                                placeholder="Enter target text..."
                                className="text-right"
                                dir="rtl"
                            />
                        </div>
                        <div className="flex justify-end gap-2">
                            <Button
                                type="button"
                                variant="outline"
                                onClick={() => onOpenChange(false)}
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