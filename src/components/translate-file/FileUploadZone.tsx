'use client'

import {useDropzone} from 'react-dropzone';
import {FileText, X} from 'lucide-react';
import {Button} from '@/components/ui/button';
import {cn} from '@/lib/utils';

interface FileUploadZoneProps {
    selectedFile: File | null;
    onFileSelect: (file: File) => void;
    onFileRemove: () => void;
    acceptedTypes: Record<string, string[]>;
}

export function FileUploadZone({
                                   selectedFile,
                                   onFileSelect,
                                   onFileRemove,
                                   acceptedTypes
                               }: FileUploadZoneProps) {
    const {getRootProps, getInputProps, isDragActive} = useDropzone({
        onDrop: (acceptedFiles) => onFileSelect(acceptedFiles[0]),
        accept: acceptedTypes,
        maxFiles: 1,
        multiple: false
    });

    if (selectedFile) {
        return (
            <div className="relative text-center p-6 bg-muted/10 rounded-lg">
                <Button
                    variant="ghost"
                    size="icon"
                    className="absolute top-2 right-2"
                    onClick={onFileRemove}
                >
                    <X className="h-4 w-4"/>
                </Button>
                <FileText className="h-12 w-12 mx-auto mb-2 text-muted-foreground"/>
                <div className="text-lg font-medium mb-2">{selectedFile.name}</div>
                <div className="text-sm text-muted-foreground">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </div>
            </div>
        );
    }

    return (
        <div
            {...getRootProps()}
            className={cn(
                "border-2 border-dashed rounded-lg p-8 text-center space-y-4 cursor-pointer",
                isDragActive && "border-primary bg-primary/5"
            )}
        >
            <input {...getInputProps()} />
            <FileText className="h-12 w-12 mx-auto text-muted-foreground"/>
            <div>
                <p className="text-muted-foreground mb-1">
                    Drag and drop a file here, or click to select
                </p>
                <p className="text-sm text-muted-foreground">
                    Supported formats: .doc, .docx, .pdf
                </p>
            </div>
            <Button
                type="button"
                variant="default"
                className="bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white"
            >
                Select files
            </Button>
        </div>
    );
} 