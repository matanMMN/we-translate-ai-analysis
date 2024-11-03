'use client'

import * as React from 'react'
import { useDropzone } from 'react-dropzone'
import { FileText, Download, Share2, X } from 'lucide-react'
import { toast } from 'sonner'

import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'

const ACCEPTED_FILE_TYPES = {
    'application/pdf': ['.pdf'],
    'application/msword': ['.doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
}

export default function TranslateFile() {
    const [selectedFile, setSelectedFile] = React.useState<File | null>(null)
    const [isTranslated, setIsTranslated] = React.useState(false)
    const [sourceLanguage, setSourceLanguage] = React.useState('')
    const [targetLanguage, setTargetLanguage] = React.useState('')

    const onDrop = React.useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
        if (rejectedFiles.length > 0) {
            toast.error('Please upload only .doc, .docx, or .pdf files')
            return
        }
        setSelectedFile(acceptedFiles[0])
    }, [])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: ACCEPTED_FILE_TYPES,
        maxFiles: 1,
        multiple: false
    })

    const handleTranslate = () => {
        if (!selectedFile) {
            toast.error('Please select a file first')
            return
        }
        if (!sourceLanguage || !targetLanguage) {
            toast.error('Please select both source and target languages')
            return
        }
        setIsTranslated(true)
    }

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0]
        if (!file) return

        const fileType = file.type
        if (!Object.keys(ACCEPTED_FILE_TYPES).includes(fileType)) {
            toast.error('Please upload only .doc, .docx, or .pdf files')
            return
        }

        setSelectedFile(file)
    }

    const removeFile = () => {
        setSelectedFile(null)
        setIsTranslated(false)
    }

    return (
        <div className="container mx-auto p-4 max-w-4xl">
            {!isTranslated ? (
                <div className="space-y-6">
                    <div className="grid grid-cols-2 gap-4">
                        <Select value={sourceLanguage} onValueChange={setSourceLanguage}>
                            <SelectTrigger>
                                <SelectValue placeholder="Select source language" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="en">English</SelectItem>
                                <SelectItem value="he">Hebrew</SelectItem>
                            </SelectContent>
                        </Select>
                        <Select value={targetLanguage} onValueChange={setTargetLanguage}>
                            <SelectTrigger>
                                <SelectValue placeholder="Select target language" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="en">English</SelectItem>
                                <SelectItem value="he">Hebrew</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    {selectedFile ? (
                        <div className="relative text-center p-6 bg-muted/10 rounded-lg">
                            <Button
                                variant="ghost"
                                size="icon"
                                className="absolute top-2 right-2"

                                onClick={removeFile}
                            >
                                <X className="h-4 w-4" />
                            </Button>
                            <FileText className="h-12 w-12 mx-auto mb-2 text-muted-foreground" />
                            <div className="text-lg font-medium mb-2">{selectedFile.name}</div>
                            <div className="text-sm text-muted-foreground">
                                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                            </div>
                        </div>
                    ) : (
                        <div
                            {...getRootProps()}
                            className={cn(
                                "border-2 border-dashed rounded-lg p-8 text-center space-y-4 cursor-pointer",
                                isDragActive && "border-primary bg-primary/5"
                            )}
                        >
                            <input {...getInputProps()} />
                            <FileText className="h-12 w-12 mx-auto text-muted-foreground" />
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
                                className="bg-[#1D3B34] hover:bg-[#1D3B34]/90"
                                onClick={(e) => {
                                    e.stopPropagation()
                                    document.getElementById('file-input')?.click()
                                }}
                            >
                                Select files
                            </Button>
                            <input
                                id="file-input"
                                type="file"
                                className="hidden"
                                accept=".doc,.docx,.pdf"
                                onChange={handleFileSelect}
                            />
                        </div>
                    )}

                    <Button
                        onClick={handleTranslate}
                        className="w-full bg-[#1D3B34] hover:bg-[#1D3B34]/90"
                        disabled={!selectedFile || !sourceLanguage || !targetLanguage}
                    >
                        Translate
                    </Button>
                </div>
            ) : (
                <h1>TODO</h1>
                // ... (previous translated view remains the same)
            )}
        </div>
    )
}