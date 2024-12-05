'use client'

import {useEffect, useState} from 'react'
import mammoth from 'mammoth'
import {Loader2} from 'lucide-react'
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card"
import {ScrollArea} from "@/components/ui/scroll-area"
import Link from "next/link";
import {copyTextToSideBySide} from "@/services/editorService";
import {toast} from "sonner";
import {selectSession} from "@/store/slices/sessionSlice";
import {useAppSelector} from "@/hooks/useAppSelector";
import {useAppDispatch} from "@/hooks/useAppDispatch";
import {useRouter} from "next/navigation";
import {Button} from "@/components/ui/button";


export default function SourceFile({file}: { file: File | null }) {
    const [htmlContent, setHtmlContent] = useState<string>('')
    const [isLoading, setIsLoading] = useState<boolean>(true)
    const [error, setError] = useState<string | null>(null)
    const {project} = useAppSelector(selectSession);
    const dispatch = useAppDispatch()
    const router = useRouter()
    useEffect(() => {
        const convertDocxToHtml = async () => {
            setIsLoading(true)
            setError(null)

            try {
                const arrayBuffer = await file?.arrayBuffer()
                if (!arrayBuffer)
                    throw new Error('Error reading the file. Please try again.')

                const result = await mammoth.convertToHtml({arrayBuffer})
                setHtmlContent(result.value)
            } catch (err) {
                setError('Error processing the file. Please try again.')
                console.error(err)
            } finally {
                setIsLoading(false)
            }
        }
        if (file)
            convertDocxToHtml()
    }, [file])


    const onCopyToSide = async () => {
        const selectedText = window.getSelection()?.toString() ?? '';
        if (/\S/.test(selectedText)) {
            try {

                const success = await copyTextToSideBySide({
                    text: selectedText,
                    sourceLanguage: project?.source_language ?? 'he',
                    dispatch,
                    projectId: project?.id as string
                });
                if (success) {
                    toast.success('Text copied to Side by Side');
                    router.push('side-by-side');
                } else {
                    toast.error('Failed to copy text');
                }
            } catch (error) {
                console.error('Error in copy to side-by-side:', error);
                toast.error('Failed to copy text');
            }
        } else {
            toast.error('Please select some text first');
        }
    }


    if (isLoading && file) {
        return (
            <Card className="w-full max-w-4xl mx-auto">
                <CardContent className="flex items-center justify-center h-96">
                    <Loader2 className="h-8 w-8 animate-spin text-primary"/>
                </CardContent>
            </Card>
        )
    }

    if (error) {
        return (
            <Card className="w-full max-w-4xl mx-auto">
                <CardContent className="flex items-center justify-center h-96">
                    <p className="text-red-500">{error}</p>
                </CardContent>
            </Card>
        )
    }


    if (!file) {
        return (
            <div className="flex items-center justify-center h-[calc(100vh-300px)]">
                <p className="text-gray-500 whitespace-pre-line text-center">No source file found.
                    Upload one through the <Link className="font-semibold underline"
                                                 href={'translate-file'}>{"Translate File"}</Link> tab</p>
            </div>
        );
    }

    return (
        <Card className="mb-8 w-full max-w-4xl mx-auto">
            <CardHeader className="pb-0">
                <CardTitle>{"Source File"}</CardTitle>
            </CardHeader>
            <div className="flex justify-center pb-6 content-center">
                <Button onClick={onCopyToSide} className="text-white">Copy to Side by side</Button>
            </div>
            <CardContent>
                <ScrollArea className="h-[calc(100vh-12rem)] max-h-[calc(100dvh-400px)] rounded-md border p-4">
                    <div
                        dir="rtl"
                        dangerouslySetInnerHTML={{__html: htmlContent}}
                        className="prose prose-sm sm:prose lg:prose-lg xl:prose-xl max-w-none"
                    />
                </ScrollArea>
            </CardContent>
        </Card>
    )
}