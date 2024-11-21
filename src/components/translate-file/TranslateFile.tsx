'use client'

import {useState} from 'react'
import {toast} from 'sonner'
import {FileText, XCircle} from 'lucide-react'
import {Button} from '@/components/ui/button'
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from '@/components/ui/select'
import {FileUploadZone} from './FileUploadZone'
import {ConfirmDialog} from './ConfirmDialog'
import {detectFileLanguage} from '@/actions/detectLanguage'
import {translateFile} from '@/actions/translateFile'
import {useAppDispatch} from '@/hooks/useAppDispatch'
import {useAppSelector} from '@/hooks/useAppSelector'
import {setTranslatedFile} from '@/store/slices/projectSlice'
import {useRouter} from 'next/navigation'
import {useSession} from "next-auth/react";
import {selectSession} from "@/store/slices/sessionSlice";
import {clearAllLocalStorage} from "@/store/slices/projectCacheSlice";

const ACCEPTED_FILE_TYPES = {
    // 'application/pdf': ['.pdf'],
    // 'application/msword': ['.doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    // 'text/plain': ['.txt']
}

type TranslationState = 'idle' | 'uploading' | 'translating' | 'completed' | 'error';

export default function TranslateFile() {
    const dispatch = useAppDispatch()
    const {data: session} = useSession()
    const router = useRouter()
    const {projectId, project} = useAppSelector(selectSession)
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [detectedLanguage, setDetectedLanguage] = useState<string | null>(null)
    const [targetLanguage, setTargetLanguage] = useState('')
    const [translationState, setTranslationState] = useState<TranslationState>('idle')
    const [showConfirmDialog, setShowConfirmDialog] = useState(false)
    const [error, setError] = useState<string | null>(null)


    const handleFileSelect = async (file: File) => {

        try {
            setSelectedFile(file)
            const formData = new FormData()
            formData.append('file', file)
            const language = await detectFileLanguage(formData)
            setDetectedLanguage(language)
            setError(null)
        } catch (error) {
            console.error(error)
            setError(`Failed to detect file language`)
            toast.error('Failed to detect file language')
        }
    }

    const handleTranslate = async () => {

        if (!selectedFile || !detectedLanguage || !targetLanguage || !projectId) {
            toast.error('Missing required data')
            return
        }

        setShowConfirmDialog(false)
        setTranslationState('translating')
        setError(null)

        try {
            const formData = new FormData()
            formData.append('file', selectedFile)


            const response = await translateFile(formData, detectedLanguage, targetLanguage, projectId, session!, project!.data)

            if (response.success) {
                if (response.mockBlob) {
                }

                if (response.mockBlob && response.blobType) {
                    dispatch(setTranslatedFile({
                        fileId: response.fileId || "1",
                        blob: response.mockBlob as Blob,
                        type: response.blobType
                    }))
                } else {
                    throw new Error("Blob couldn't be extracted")
                }

                setTranslationState('completed')
                dispatch(clearAllLocalStorage({projectId}))
                setTimeout(() => {
                    router.push('editor')
                }, 1250)
            } else {
                throw new Error(response.error || 'Translation failed')
            }
        } catch (error) {
            setTranslationState('error')
            setError(error instanceof Error ? error.message : 'Translation failed')
            toast.error('Translation failed. Please try again.')
        }
    }

    if (translationState === 'error') {
        return (
            <div className="container mx-auto p-4 max-w-4xl">
                <div className="text-center p-6 bg-destructive/10 rounded-lg space-y-4">
                    <XCircle className="h-12 w-12 mx-auto text-destructive"/>
                    <h2 className="text-2xl font-semibold text-destructive">Translation Failed</h2>
                    <p className="text-muted-foreground">
                        {error || 'An unexpected error occurred during translation.'}
                    </p>
                    <div className="space-x-4">
                        <Button
                            variant="outline"
                            onClick={() => {
                                setTranslationState('idle')
                                setError(null)
                            }}
                        >
                            Try Again
                        </Button>
                        <Button
                            variant="destructive"
                            onClick={() => router.push(`${projectId ? `/${projectId}/details` : '/'}`)}
                        >
                            Return to Dashboard
                        </Button>
                    </div>
                </div>
            </div>
        )
    }

    if (translationState === 'translating') {
        return (
            <div className="container mx-auto p-4 max-w-4xl text-center space-y-6">
                <h2 className="text-2xl font-semibold">Translating your file...</h2>
                <p className="text-muted-foreground">
                    This process could take up to 10 minutes. You must not leave this page.
                </p>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                    <div className="h-full bg-primary animate-pulse" style={{width: '100%'}}/>
                </div>
                <p className="text-sm text-muted-foreground">
                    Your translated file will be available in the editor once completed.
                    You will be redirected automatically.
                </p>
            </div>
        )
    }

    if (translationState === 'completed') {
        return (
            <div className="container mx-auto p-4 max-w-4xl">
                <div className="text-center p-6 bg-muted/10 rounded-lg space-y-4">
                    <FileText className="h-12 w-12 mx-auto text-green-600"/>
                    <h2 className="text-2xl font-semibold">Translation Complete!</h2>
                    <p className="text-muted-foreground">
                        Your file has been translated and is now available in the editor.
                    </p>
                    <Button
                        variant="outline"
                        onClick={() => setTranslationState('idle')}
                    >
                        Translate another file
                    </Button>
                </div>
            </div>
        )
    }

    return (
        <>
            <div className="container mx-auto p-4 max-w-4xl">
                <div className="space-y-6">
                    {error && (
                        <div className="p-4 bg-destructive/10 rounded-lg">
                            <p className="text-sm text-destructive font-medium">
                                {error}
                            </p>
                        </div>
                    )}

                    {detectedLanguage && (
                        <div className="p-4 bg-muted rounded-lg">
                            <p className="text-sm text-muted-foreground">
                                Detected source language: <span className="font-medium">{detectedLanguage}</span>
                            </p>
                        </div>
                    )}

                    <Select
                        value={targetLanguage}
                        onValueChange={setTargetLanguage}
                        onOpenChange={() => setError(null)} // Clear error when user tries again
                    >
                        <SelectTrigger>
                            <SelectValue placeholder="Select target language"/>
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="en">English</SelectItem>
                            <SelectItem value="he">Hebrew</SelectItem>
                        </SelectContent>
                    </Select>

                    <FileUploadZone
                        selectedFile={selectedFile}
                        onFileSelect={handleFileSelect}
                        onFileRemove={() => {
                            setSelectedFile(null)
                            setDetectedLanguage(null)
                            setError(null) // Clear error when file is removed
                        }}
                        acceptedTypes={ACCEPTED_FILE_TYPES}
                        // error={error} // Pass error to FileUploadZone
                    />

                    <Button
                        onClick={() => setShowConfirmDialog(true)}
                        className="w-full bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white"
                        disabled={!selectedFile || !targetLanguage || !!error}
                    >
                        Translate
                    </Button>
                </div>
            </div>

            <ConfirmDialog
                open={showConfirmDialog}
                onOpenChange={setShowConfirmDialog}
                onConfirm={handleTranslate}
            />
        </>
    )
}