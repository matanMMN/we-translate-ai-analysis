'use client'

import * as React from 'react'
import { FileIcon, AlertCircle, CheckCircle2, Upload } from 'lucide-react'
import { useDropzone } from 'react-dropzone'
import { toast } from 'sonner'

import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { validateFile, formatFileSize, MAX_FILE_SIZE } from '@/lib/fileUtils'

interface UploadModalProps {
    open: boolean
    onClose: () => void
    onUpload: (files: File[]) => void
}

interface FileStatus {
    file: File
    status: 'validating' | 'valid' | 'invalid'
    error?: string
}

export default function UploadFileModal({ open, onClose, onUpload }: UploadModalProps) {
    const [fileStatus, setFileStatus] = React.useState<FileStatus | null>(null)

    const handleDrop = React.useCallback(async (acceptedFiles: File[]) => {
        if (acceptedFiles.length === 0) return

        const file = acceptedFiles[0] // Only handle single file
        
        // Show initial validation state
        setFileStatus({ file, status: 'validating' })

        // Simulate validation delay for UX
        await new Promise(resolve => setTimeout(resolve, 500))

        const validation = validateFile(file)
        if (!validation.valid) {
            setFileStatus({ file, status: 'invalid', error: validation.error })
            toast.error(validation.error)
            return
        }

        setFileStatus({ file, status: 'valid' })
        toast.success('File ready for upload')
    }, [])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop: handleDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'application/msword': ['.doc'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
        },
        maxFiles: 1,
        multiple: false,
        maxSize: MAX_FILE_SIZE
    })

    const handleUpload = () => {
        if (fileStatus?.status === 'valid') {
            onUpload([fileStatus.file])
            toast.success('File uploaded successfully')
        }
    }

    const handleClose = () => {
        setFileStatus(null)
        onClose()
    }

    return (
        <Dialog open={open} onOpenChange={handleClose}>
            <DialogContent className="sm:max-w-[450px]">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <Upload className="w-5 h-5" />
                        Upload Reference File
                    </DialogTitle>
                </DialogHeader>

                <div className="space-y-4">
                    <div className="text-sm text-muted-foreground text-center">
                        Supported formats: .doc, .docx, .pdf (Max {formatFileSize(MAX_FILE_SIZE)})
                    </div>

                    <div
                        {...getRootProps()}
                        className={cn(
                            "border-2 border-dashed rounded-lg transition-colors duration-200",
                            isDragActive ? "border-primary bg-primary/5" : "border-gray-200",
                            fileStatus ? "py-4" : "py-8",
                            "cursor-pointer"
                        )}
                    >
                        <input {...getInputProps()} />
                        
                        <div className="flex flex-col items-center gap-2 px-4">
                            {!fileStatus ? (
                                <>
                                    <FileIcon className="w-8 h-8 text-gray-400" />
                                    <p className="text-sm text-center text-muted-foreground">
                                        {isDragActive 
                                            ? "Drop your file here" 
                                            : "Drag and drop your file here, or click to browse"}
                                    </p>
                                </>
                            ) : (
                                <div className="w-full">
                                    <div className="flex items-center justify-between mb-2">
                                        <div className="flex items-center gap-2">
                                            <FileIcon className="w-5 h-5 text-gray-400" />
                                            <span className="text-sm font-medium truncate max-w-[200px]">
                                                {fileStatus.file.name}
                                            </span>
                                        </div>
                                        {fileStatus.status === 'validating' && (
                                            <div className="animate-pulse text-primary">
                                                Validating...
                                            </div>
                                        )}
                                        {fileStatus.status === 'valid' && (
                                            <CheckCircle2 className="w-5 h-5 text-green-500" />
                                        )}
                                        {fileStatus.status === 'invalid' && (
                                            <AlertCircle className="w-5 h-5 text-red-500" />
                                        )}
                                    </div>
                                    <div className="text-xs text-muted-foreground">
                                        {formatFileSize(fileStatus.file.size)}
                                    </div>
                                    {fileStatus.error && (
                                        <div className="text-xs text-red-500 mt-1">
                                            {fileStatus.error}
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>

                    <div className="flex gap-2">
                        <Button
                            variant="outline"
                            className="flex-1"
                            onClick={handleClose}
                        >
                            Cancel
                        </Button>
                        <Button
                            className="flex-1 bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white"
                            onClick={handleUpload}
                            disabled={!fileStatus || fileStatus.status !== 'valid'}
                        >
                            Upload
                        </Button>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    )
}