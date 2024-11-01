'use client'

import * as React from 'react'
import { ThumbsUp, ThumbsDown, ChevronDown, Plus, X, Check } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { toast } from 'sonner'

interface EditorSection {
    id: string
    sourceContent: string
    targetContent: string
}

export default function SideBySide() {
    const [sourceLanguage, setSourceLanguage] = React.useState('')
    const [targetLanguage] = React.useState('Hebrew')
    const [sections, setSections] = React.useState<EditorSection[]>([
        { id: '1', sourceContent: '', targetContent: '' },
        { id: '2', sourceContent: '', targetContent: '' },
    ])
    const [isGlossaryOpen, setIsGlossaryOpen] = React.useState(false)
    const [glossarySource, setGlossarySource] = React.useState('')
    const [glossaryTarget, setGlossaryTarget] = React.useState('')
    const [sourceGlossaryLang, setSourceGlossaryLang] = React.useState('en')
    const [targetGlossaryLang, setTargetGlossaryLang] = React.useState('he')
    const [activeSection, setActiveSection] = React.useState('1')

    const handleAddSection = () => {
        const newId = (sections.length + 1).toString()
        setSections([...sections, { id: newId, sourceContent: '', targetContent: '' }])
    }

    const handleTranslate = async () => {
        // Simulating translation process
        toast.promise(
            new Promise((resolve) => setTimeout(resolve, 2000)),
            {
                loading: 'Translating...',
                success: 'Translation completed!',
                error: 'Translation failed.',
            }
        )
    }

    const handleGlossarySubmit = () => {
        if (!glossarySource || !glossaryTarget) {
            toast.error('Please fill in both source and target text')
            return
        }
        // Here you would typically save the glossary entry
        toast.success('Glossary entry added successfully!')
        setIsGlossaryOpen(false)
        setGlossarySource('')
        setGlossaryTarget('')
    }

    return (
        <div className="flex h-[calc(100vh-120px)]">
            {/* Section Navigation */}
            <div className="w-12 border-r bg-background flex flex-col items-center py-4 space-y-2">
                {sections.map((section) => (
                    <Button
                        key={section.id}
                        variant={activeSection === section.id ? "default" : "ghost"}
                        className="w-8 h-8 rounded-full"
                        onClick={() => setActiveSection(section.id)}
                    >
                        {section.id}
                    </Button>
                ))}
                <Button
                    variant="ghost"
                    className="w-8 h-8 rounded-full mt-auto"
                    onClick={handleAddSection}
                >
                    <Plus className="h-4 w-4" />
                </Button>
            </div>

            {/* Main Content */}
            <div className="flex-1 flex flex-col p-4">
                <div className="grid grid-cols-2 gap-4 mb-4">
                    <Select value={sourceLanguage} onValueChange={setSourceLanguage}>
                        <SelectTrigger className="bg-gray-50">
                            <SelectValue placeholder="Select language" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="en">English</SelectItem>
                            <SelectItem value="he">Hebrew</SelectItem>
                        </SelectContent>
                    </Select>
                    <div className="bg-gray-50 rounded-md px-4 py-2 flex items-center justify-between">
                        {targetLanguage}
                        <ChevronDown className="h-4 w-4 text-gray-500" />
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-4 flex-1">
                    {/* Source Editor */}
                    <div className="flex flex-col">
                        <div className="bg-gray-50 rounded-t-md p-2 border-b">
                            <div className="flex items-center gap-2">
                                <select className="bg-transparent px-2 py-1 border rounded text-sm">
                                    <option>Arial</option>
                                </select>
                                <select className="bg-transparent px-2 py-1 border rounded text-sm">
                                    <option>Normal</option>
                                </select>
                                <div className="flex items-center border rounded">
                                    <button className="px-2 py-1 hover:bg-gray-100">B</button>
                                    <button className="px-2 py-1 hover:bg-gray-100">I</button>
                                    <button className="px-2 py-1 hover:bg-gray-100">U</button>
                                    <button className="px-2 py-1 hover:bg-gray-100">S</button>
                                </div>
                                <div className="flex items-center border rounded">
                                    <button className="px-2 py-1 hover:bg-gray-100">x²</button>
                                    <button className="px-2 py-1 hover:bg-gray-100">x₂</button>
                                </div>
                                <div className="flex items-center border rounded">
                                    <button className="px-2 py-1 hover:bg-gray-100">
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <line x1="21" y1="6" x2="3" y2="6"></line>
                                            <line x1="21" y1="12" x2="3" y2="12"></line>
                                            <line x1="21" y1="18" x2="3" y2="18"></line>
                                        </svg>
                                    </button>
                                    <button className="px-2 py-1 hover:bg-gray-100">
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <line x1="18" y1="6" x2="3" y2="6"></line>
                                            <line x1="15" y1="12" x2="3" y2="12"></line>
                                            <line x1="12" y1="18" x2="3" y2="18"></line>
                                        </svg>
                                    </button>
                                    <button className="px-2 py-1 hover:bg-gray-100">
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <line x1="3" y1="6" x2="21" y2="6"></line>
                                            <line x1="6" y1="12" x2="21" y2="12"></line>
                                            <line x1="9" y1="18" x2="21" y2="18"></line>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div className="flex-1 border rounded-b-md p-4">
              <textarea
                  className="w-full h-full resize-none border-0 focus:outline-none bg-transparent"
                  placeholder="Enter source text..."
                  value={sections.find(s => s.id === activeSection)?.sourceContent || ''}
                  onChange={(e) => {
                      setSections(sections.map(s =>
                          s.id === activeSection
                              ? { ...s, sourceContent: e.target.value }
                              : s
                      ))
                  }}
              />
                        </div>
                    </div>

                    {/* Target Editor */}
                    <div className="flex flex-col">
                        <div className="bg-gray-50 rounded-t-md p-2 border-b">
                            <div className="flex items-center gap-2">
                                <select className="bg-transparent px-2 py-1 border rounded text-sm">
                                    <option>Arial</option>
                                </select>
                                <select className="bg-transparent px-2 py-1 border rounded text-sm">
                                    <option>Normal</option>
                                </select>
                                <div className="flex items-center border rounded">
                                    <button className="px-2 py-1 hover:bg-gray-100">B</button>
                                    <button className="px-2 py-1 hover:bg-gray-100">I</button>
                                    <button className="px-2 py-1 hover:bg-gray-100">U</button>
                                    <button className="px-2 py-1 hover:bg-gray-100">S</button>
                                </div>
                                <div className="flex items-center border rounded">
                                    <button className="px-2 py-1 hover:bg-gray-100">x²</button>
                                    <button className="px-2 py-1 hover:bg-gray-100">x₂</button>
                                </div>
                                <div className="flex items-center border rounded">
                                    <button className="px-2 py-1 hover:bg-gray-100">
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <line x1="21" y1="6" x2="3" y2="6"></line>
                                            <line x1="21" y1="12" x2="3" y2="12"></line>
                                            <line x1="21" y1="18" x2="3" y2="18"></line>
                                        </svg>
                                    </button>
                                    <button className="px-2 py-1 hover:bg-gray-100">
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <line x1="18" y1="6" x2="3" y2="6"></line>
                                            <line x1="15" y1="12" x2="3" y2="12"></line>
                                            <line x1="12" y1="18" x2="3" y2="18"></line>
                                        </svg>
                                    </button>
                                    <button className="px-2 py-1 hover:bg-gray-100">
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <line x1="3" y1="6" x2="21" y2="6"></line>
                                            <line x1="6" y1="12" x2="21" y2="12"></line>
                                            <line x1="9" y1="18" x2="21" y2="18"></line>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div className="flex-1 border rounded-b-md p-4">
              <textarea
                  className="w-full h-full resize-none border-0 focus:outline-none bg-transparent"
                  placeholder="Enter target text..."
                  value={sections.find(s => s.id === activeSection)?.targetContent || ''}
                  onChange={(e) => {
                      setSections(sections.map(s =>
                          s.id === activeSection
                              ? { ...s, targetContent: e.target.value }
                              : s
                      ))
                  }}
              />
                        </div>
                    </div>
                </div>

                <div className="flex justify-between items-center mt-4">
                    <div className="flex gap-2">
                        <Button variant="ghost" size="icon" className="rounded-full">
                            <ThumbsUp className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon" className="rounded-full">
                            <ThumbsDown className="h-4 w-4" />
                        </Button>
                    </div>
                    <div className="flex gap-2">
                        <Button
                            className="bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white px-8"
                            onClick={handleTranslate}
                        >
                            Translate
                        </Button>
                        <Button
                            variant="secondary"
                            onClick={() => setIsGlossaryOpen(true)}
                        >
                            Glossary
                        </Button>
                    </div>
                </div>
            </div>

            {/* Glossary Modal */}
            <Dialog open={isGlossaryOpen} onOpenChange={setIsGlossaryOpen}>
                <DialogContent className="sm:max-w-[500px]">
                    <DialogHeader>
                        <div className="flex items-center justify-between">
                            <DialogTitle>Glossary</DialogTitle>
                            <Button
                                variant="ghost"
                                size="icon"
                                className="h-6 w-6 rounded-full"
                                onClick={() => setIsGlossaryOpen(false)}
                            >
                                <X className="h-4 w-4" />
                            </Button>
                        </div>
                    </DialogHeader>
                    <div className="space-y-4 pt-4">
                        <div className="flex items-center justify-between">
                            <Select
                                value="default"
                                onValueChange={() => {}}
                            >
                                <SelectTrigger className="w-[200px]">
                                    <SelectValue placeholder="Default glossary" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="default">Default glossary</SelectItem>
                                </SelectContent>
                            </Select>
                            <Button variant="link" className="text-blue-500 p-0">
                                Add new glossary
                            </Button>
                        </div>

                        <div className="grid gap-4">
                            <div className="flex gap-4">
                                <div className="flex-1">
                                    <Select value={sourceGlossaryLang} onValueChange={setSourceGlossaryLang}>
                                        <SelectTrigger>
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="en">EN</SelectItem>
                                            <SelectItem value="de">DE</SelectItem>
                                            <SelectItem value="he">HE</SelectItem>

                                        </SelectContent>
                                    </Select>
                                </div>
                                <div className="flex-[3]">
                                    <Input
                                        placeholder="Source text"
                                        value={glossarySource}
                                        onChange={(e) => setGlossarySource(e.target.value)}
                                    />
                                </div>
                            </div>

                            <div className="flex gap-4">
                                <div className="flex-1">
                                    <Select value={targetGlossaryLang} onValueChange={setTargetGlossaryLang}>
                                        <SelectTrigger>
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="en">EN</SelectItem>
                                            <SelectItem value="de">DE</SelectItem>
                                            <SelectItem value="he">HE</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                                <div className="flex-[3] relative">
                                    <Input
                                        placeholder="Target text"
                                        value={glossaryTarget}
                                        onChange={(e) => setGlossaryTarget(e.target.value)}
                                    />
                                    <Button
                                        className="absolute right-[-48px] top-0 bg-[#008DB9] hover:bg-[#008DB9]/90"
                                        size="icon"
                                        onClick={handleGlossarySubmit}
                                    >
                                        <Check className="h-4 w-4" />
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    )
}