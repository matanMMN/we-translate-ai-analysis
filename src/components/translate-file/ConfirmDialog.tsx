'use client'

import {AlertTriangle} from 'lucide-react';
import {Button} from '@/components/ui/button';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from '@/components/ui/dialog';

interface ConfirmDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    onConfirm: () => void;
}

export function ConfirmDialog({open, onOpenChange, onConfirm}: ConfirmDialogProps) {
    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Confirm Translation</DialogTitle>
                    <DialogDescription asChild>
                        <div className="space-y-4">
                            <p>
                                Are you sure you want to translate this file? This will:
                            </p>
                            <ul className="list-disc list-inside space-y-2">
                                <li>Replace your current editor file</li>
                                <li>Take approximately 5 minutes to complete</li>
                                <li>Cannot be cancelled once started</li>
                            </ul>
                            <div className="flex items-center gap-2 p-4 bg-yellow-50 rounded-lg">
                                <AlertTriangle className="h-5 w-5 text-yellow-600"/>
                                <p className="text-sm text-yellow-600">
                                    This action cannot be undone.
                                </p>
                            </div>
                        </div>
                    </DialogDescription>
                </DialogHeader>
                <DialogFooter>
                    <Button variant="outline" onClick={() => onOpenChange(false)}>
                        Cancel
                    </Button>
                    <Button
                        onClick={onConfirm}
                        className="bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white"
                    >
                        Confirm Translation
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
} 