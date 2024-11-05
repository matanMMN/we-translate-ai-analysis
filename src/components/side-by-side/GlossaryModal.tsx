'use client'

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { addGlossaryEntry } from '@/services/glossaryService';
import { toast } from 'sonner';
import { GlossaryList } from './GlossaryList';

interface GlossaryModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    sourceLang: string;
    targetLang: string;
}

export function GlossaryModal({ 
    open, 
    onOpenChange,
    sourceLang,
    targetLang 
}: GlossaryModalProps) {
    const [sourceText, setSourceText] = useState('');
    const [targetText, setTargetText] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

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
                targetLang
            });

            // Reset form
            setSourceText('');
            setTargetText('');
            onOpenChange(false);
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
                    <GlossaryList sourceLang={sourceLang} targetLang={targetLang} />
                    
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="sourceText">Source Text</Label>
                            <Input
                                id="sourceText"
                                value={sourceText}
                                onChange={(e) => setSourceText(e.target.value)}
                                placeholder="Enter source text..."
                                className={sourceLang === 'he' ? 'text-right' : 'text-left'}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="targetText">Target Text</Label>
                            <Input
                                id="targetText"
                                value={targetText}
                                onChange={(e) => setTargetText(e.target.value)}
                                placeholder="Enter target text..."
                                className="text-right" // Hebrew is always RTL
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