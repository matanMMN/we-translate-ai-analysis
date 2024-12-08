'use client'

import { useEffect, useState } from 'react'
import mammoth from 'mammoth'
import { Loader2 } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"


export default function ReferenceFile({ file }: { file: File | null }) {
    const [htmlContent, setHtmlContent] = useState<string>('')
    const [isLoading, setIsLoading] = useState<boolean>(true)
    const [error, setError] = useState<string | null>(null)
    
    useEffect(() => {
        const convertDocxToHtml = async () => {
            setIsLoading(true)
            setError(null)

            try {
                const arrayBuffer = await file?.arrayBuffer()
                if (!arrayBuffer)
                    throw new Error('Error reading the file. Please try again.')

                const result = await mammoth.convertToHtml({ arrayBuffer })
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

    if (isLoading) {
        return (
            <Card className="w-full max-w-4xl mx-auto">
                <CardContent className="flex items-center justify-center h-96">
                    <Loader2 className="h-8 w-8 animate-spin text-primary" />
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

    return (
        <Card className="mb-8 w-full max-w-4xl mx-auto">
            <CardHeader>
                <CardTitle>{"Reference File"}</CardTitle>
            </CardHeader>
            <CardContent>
                <ScrollArea className="h-[calc(100vh-12rem)] max-h-[calc(100dvh-400px)] rounded-md border p-4">
                    <div
                        dangerouslySetInnerHTML={{ __html: htmlContent }}
                        className="prose prose-sm sm:prose lg:prose-lg xl:prose-xl max-w-none"
                    />
                </ScrollArea>
            </CardContent>
        </Card>
    )
}