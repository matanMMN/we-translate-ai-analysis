'use client'

import * as React from 'react'
import { FileIcon, Search } from 'lucide-react'
import { useDropzone } from 'react-dropzone'
import { format } from 'date-fns'

import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
    ContextMenu,
    ContextMenuContent,
    ContextMenuItem,
    ContextMenuTrigger,
} from '@/components/ui/context-menu'

interface UploadModalProps {
    open: boolean
    onClose: () => void
    onUpload: (files: File[]) => void
}

interface ExistingFile {
    id: string
    name: string
    date: Date
}

export default function Component({ open, onClose, onUpload }: UploadModalProps = {
    open: true,
    onClose: () => {},
    onUpload: () => {}
}) {
    const [activeTab, setActiveTab] = React.useState('desktop')
    const [searchQuery, setSearchQuery] = React.useState('')
    const [selectedFiles, setSelectedFiles] = React.useState<File[]>([])
    const [sortOrder, setSortOrder] = React.useState<'asc' | 'desc'>('desc')

    // Simulated existing files
    const existingFiles: ExistingFile[] = React.useMemo(() =>
            Array.from({ length: 10 }, (_, i) => ({
                id: `file-${i}`,
                name: 'Fostimon',
                date: new Date(2024, 5, 7) // July 6, 2024
            }))
        , [])

    const filteredFiles = React.useMemo(() => {
        const files = existingFiles.filter(file =>
            file.name.toLowerCase().includes(searchQuery.toLowerCase())
        )

        return files.sort((a, b) =>
            sortOrder === 'desc'
                ? b.date.getTime() - a.date.getTime()
                : a.date.getTime() - b.date.getTime()
        )
    }, [existingFiles, searchQuery, sortOrder])

    const onDrop = React.useCallback((acceptedFiles: File[]) => {
        setSelectedFiles(acceptedFiles)
    }, [])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'application/msword': ['.doc'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
        }
    })

    const handleUpload = () => {
        onUpload(selectedFiles)
        onClose()
    }

    const handleDelete = (fileId: string) => {
        // In a real app, you would call an API to delete the file
        console.log('Deleting file:', fileId)
    }

    return (
        <Dialog open={open} onOpenChange={onClose}>
            <DialogContent className="">
                <DialogHeader>
                    <div className="flex items-center justify-between">
                        <DialogTitle>Upload reference file</DialogTitle>
                    </div>
                </DialogHeader>
                <div className="space-y-4 pt-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                        <Input
                            placeholder="Search reference file:"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="pl-9 bg-gray-50"
                        />
                    </div>

                    <Tabs value={activeTab} onValueChange={setActiveTab}>
                        <TabsList className="grid w-full grid-cols-2">
                            <TabsTrigger value="desktop">From your desktop</TabsTrigger>
                            <TabsTrigger value="existing">From existing list</TabsTrigger>
                        </TabsList>

                        <TabsContent value="desktop" className="space-y-4">
                            <div className="text-sm text-muted-foreground text-center">
                                Supported file formats: .doc, .docx, .pdf
                            </div>
                            <div
                                {...getRootProps()}
                                className={cn(
                                    "border-2 border-dashed rounded-lg p-8 text-center space-y-4",
                                    isDragActive && "border-[#1D3B34] bg-[#1D3B34]/5"
                                )}
                            >
                                <input {...getInputProps()} />
                                <div className="text-sm text-muted-foreground">
                                    Drag and drop your files here
                                </div>
                                <Button
                                    variant="default"
                                    className="bg-[#1D3B34] hover:bg-[#1D3B34]/90"
                                >
                                    Select files
                                </Button>
                            </div>
                        </TabsContent>

                        <TabsContent value="existing" className="space-y-4">
                            <div className="flex items-center justify-between">
                <span className="text-sm font-medium">
                  Newest {sortOrder === 'desc' ? '↑' : '↓'}
                </span>
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => setSortOrder(current => current === 'desc' ? 'asc' : 'desc')}
                                >
                                    Sort
                                </Button>
                            </div>
                            <div className="grid grid-cols-3 gap-4 max-h-[300px] overflow-y-auto">
                                {filteredFiles.map((file) => (
                                    <ContextMenu key={file.id}>
                                        <ContextMenuTrigger>
                                            <div className="p-4 rounded-lg bg-gray-50 space-y-2 text-center hover:bg-gray-100 transition-colors">
                                                <FileIcon className="h-8 w-8 mx-auto text-[#1D3B34]" />
                                                <div className="text-sm font-medium truncate">
                                                    {file.name}
                                                </div>
                                                <div className="text-xs text-muted-foreground">
                                                    {format(file.date, 'MM/dd/yy')}
                                                </div>
                                            </div>
                                        </ContextMenuTrigger>
                                        <ContextMenuContent>
                                            <ContextMenuItem
                                                className="text-red-600"
                                                onClick={() => handleDelete(file.id)}
                                            >
                                                Delete
                                            </ContextMenuItem>
                                        </ContextMenuContent>
                                    </ContextMenu>
                                ))}
                            </div>
                        </TabsContent>
                    </Tabs>

                    <Button
                        className="w-full bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white"
                        onClick={handleUpload}
                    >
                        Upload
                    </Button>
                </div>
            </DialogContent>
        </Dialog>
    )
}