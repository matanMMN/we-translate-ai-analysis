'use client'

import * as React from 'react'
import { Download, Share2, ZoomIn, ZoomOut, RotateCw, ChevronLeft, ChevronRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Slider } from '@/components/ui/slider'

export default function ReferenceFile() {
    const [scale, setScale] = React.useState(100)
    const [currentPage, setCurrentPage] = React.useState(1)
    const totalPages = 10 // This would come from your PDF document

    const handleZoomIn = () => setScale(prev => Math.min(200, prev + 10))
    const handleZoomOut = () => setScale(prev => Math.max(50, prev - 10))

    return (
        <div className="h-[calc(100vh-120px)] flex flex-col">
            <div className="flex justify-between items-center mb-4">
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-2">
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={handleZoomOut}
                            className="h-8 w-8"
                        >
                            <ZoomOut className="h-4 w-4" />
                        </Button>
                        <span className="min-w-[4rem] text-center">{scale}%</span>
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={handleZoomIn}
                            className="h-8 w-8"
                        >
                            <ZoomIn className="h-4 w-4" />
                        </Button>
                    </div>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                        <RotateCw className="h-4 w-4" />
                    </Button>
                </div>

                <div className="flex items-center gap-2">
                    <Button variant="outline" className="gap-2">
                        <Share2 className="h-4 w-4" />
                        Share
                    </Button>
                    <Button className="gap-2 bg-[#1D3B34] hover:bg-[#1D3B34]/90">
                        <Download className="h-4 w-4" />
                        Download
                    </Button>
                </div>
            </div>

            <Card className="flex-1 relative">
                <div className="absolute inset-0 flex items-center justify-center bg-gray-50">
                    {/* PDF Viewer will be mounted here */}
                    <div className="text-center text-muted-foreground">
                        PDF Preview
                    </div>
                </div>

                <div className="absolute left-4 top-1/2 -translate-y-1/2">
                    <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 bg-white shadow-lg rounded-full"
                        onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                        disabled={currentPage === 1}
                    >
                        <ChevronLeft className="h-4 w-4" />
                    </Button>
                </div>

                <div className="absolute right-4 top-1/2 -translate-y-1/2">
                    <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 bg-white shadow-lg rounded-full"
                        onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                        disabled={currentPage === totalPages}
                    >
                        <ChevronRight className="h-4 w-4" />
                    </Button>
                </div>
            </Card>

            <div className="mt-4 flex items-center justify-center gap-4">
        <span className="text-sm text-muted-foreground">
          Page {currentPage} of {totalPages}
        </span>
                <div className="w-64">
                    <Slider
                        value={[currentPage]}
                        min={1}
                        max={totalPages}
                        step={1}
                        onValueChange={([value]) => setCurrentPage(value)}
                    />
                </div>
            </div>
        </div>
    )
}