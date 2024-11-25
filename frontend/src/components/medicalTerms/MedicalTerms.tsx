'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Search } from 'lucide-react'
import { cn } from "@/lib/utils"
import { useDebounce } from 'use-debounce'
import { AnimatePresence, motion } from "framer-motion"
import medicalTermsData from '@/assets/MedicalTerms.json'

interface MedicalTerm {
    name: string;
    englishName: string;
}

const ITEMS_PER_PAGE = 20

export function  MedicalTerms() {
    const [terms, setTerms] = useState<MedicalTerm[]>([])
    const [page, setPage] = useState(1)
    const [loading, setLoading] = useState(false)
    const [hasMore, setHasMore] = useState(true)
    const [searchQuery, setSearchQuery] = useState('')
    const [language] = useState<'hebrew' | 'english'>('english')
    const observer = useRef<IntersectionObserver>()
    const [debouncedQuery] = useDebounce(searchQuery, 100)
    const [searchResults, setSearchResults] = useState<MedicalTerm[]>([])
    const [showResults, setShowResults] = useState(false)

    useEffect(() => {
        setTerms(medicalTermsData.slice(0, ITEMS_PER_PAGE))
        setHasMore(medicalTermsData.length > ITEMS_PER_PAGE)
    }, [])

    const lastTermElementRef = useCallback((node: HTMLDivElement | null) => {
        if (loading) return
        if (observer.current) observer.current.disconnect()
        observer.current = new IntersectionObserver(entries => {
            if (entries[0].isIntersecting && hasMore) {
                setPage(prevPage => prevPage + 1)
            }
        })
        if (node) observer.current.observe(node)
    }, [loading, hasMore])

    useEffect(() => {
        if (debouncedQuery) {
            setLoading(true)
            const searchTerm = debouncedQuery.toLowerCase()
            const filteredResults = medicalTermsData.filter(term =>
                term.name.toLowerCase().includes(searchTerm) ||
                term.englishName.toLowerCase().includes(searchTerm)
            )
            
            setSearchResults(filteredResults.slice(0, 5))
            setShowResults(true)
            
            setTerms(filteredResults.slice(0, page * ITEMS_PER_PAGE))
            setHasMore(filteredResults.length > page * ITEMS_PER_PAGE)
            setLoading(false)
        } else {
            setSearchResults([])
            setShowResults(false)
            setTerms(medicalTermsData.slice(0, page * ITEMS_PER_PAGE))
            setHasMore(medicalTermsData.length > page * ITEMS_PER_PAGE)
        }
    }, [debouncedQuery, page])

    useEffect(() => {
        if (!debouncedQuery && page > 1) {
            setLoading(true)
            const newTerms = medicalTermsData.slice(0, page * ITEMS_PER_PAGE)
            setTerms(newTerms)
            setHasMore(medicalTermsData.length > page * ITEMS_PER_PAGE)
            setLoading(false)
        }
    }, [page, debouncedQuery])

    useEffect(() => {
        setPage(1)
    }, [debouncedQuery])

    return (
        <div className="container mx-auto p-4 max-w-7xl">
            {/*<h1 className="text-4xl font-bold mb-8">Medical Terms</h1>*/}

            <motion.header
                initial={{y: -20, opacity: 0}}
                animate={{y: 0, opacity: 1}}
                transition={{delay: 0.2}}
                className="p-4 flex w-full justify-center relative"
            >
                <div className="relative bg-[#F0F2F5] border-none rounded-2xl w-full max-w-2xl">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-6 h-6 text-muted-foreground"/>
                    <Input
                        placeholder="Search medical terms"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="pl-12 pr-4 py-6 text-xl w-full h-[46px] focus:outline-none focus:ring-0 focus:border-blue-500"
                    />
                    <AnimatePresence>
                        {showResults && searchResults.length > 0 && (
                            <motion.div
                                initial={{opacity: 0, y: -10}}
                                animate={{opacity: 1, y: 0}}
                                exit={{opacity: 0, y: -10}}
                                className="absolute w-full bg-background border rounded-md shadow-lg z-50"
                            >
                                {searchResults.slice(0, 5).map((result) => (
                                    <motion.div
                                        key={result.englishName}
                                        initial={{opacity: 0}}
                                        animate={{opacity: 1}}
                                        exit={{opacity: 0}}
                                        className="px-4 py-2 transition-all duration-250 hover:bg-gray-300 cursor-pointer bg-[#98A7A3]"
                                        onClick={() => {
                                            setSearchQuery(result.englishName)
                                            setShowResults(false)
                                        }}
                                    >
                                        {result.englishName.toLowerCase().indexOf(searchQuery.toLowerCase()) >= 0 && (
                                            <>
                                                <span className="font-normal text-white">
                                                    {result.englishName.slice(0, result.englishName.toLowerCase().indexOf(searchQuery.toLowerCase()))}
                                                </span>
                                                <span className="font-normal">
                                                    {result.englishName.slice(
                                                        result.englishName.toLowerCase().indexOf(searchQuery.toLowerCase()),
                                                        result.englishName.toLowerCase().indexOf(searchQuery.toLowerCase()) + searchQuery.length
                                                    )}
                                                </span>
                                                <span className="font-normal text-white">
                                                    {result.englishName.slice(result.englishName.toLowerCase().indexOf(searchQuery.toLowerCase()) + searchQuery.length)}
                                                </span>
                                            </>
                                        )}
                                    </motion.div>
                                ))}
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </motion.header>

            {/*<Tabs defaultValue="hebrew" className="mb-8" onValueChange={(value) => setLanguage(value as 'hebrew' | 'english')}>*/}
            {/*    <TabsList className="grid w-[400px] grid-cols-2">*/}
            {/*        <TabsTrigger value="hebrew">Hebrew terms</TabsTrigger>*/}
            {/*        <TabsTrigger value="english">English terms</TabsTrigger>*/}
            {/*    </TabsList>*/}
            {/*</Tabs>*/}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {terms.map((term, index) => (
                    <Card
                        key={index}
                        ref={index === terms.length - 1 ? lastTermElementRef : null}
                        className="transition-all duration-200 hover:shadow-lg"
                    >
                        <CardContent className="p-6 h-full">
                            <div className="flex flex-col gap-2 justify-between h-full">
                                <h2 className={cn(
                                    "text-2xl font-bold",
                                    language === 'hebrew' ? 'text-right' : 'text-left'
                                )}>
                                    {language === 'hebrew' ? term.name : term.englishName}
                                </h2>
                                <p className="text-muted-foreground text-right">
                                    {language === 'hebrew' ? term.englishName : term.name}
                                </p>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            {loading && (
                <div className="text-center mt-8">
                    <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-primary border-r-transparent" role="status">
                        <span className="sr-only">Loading...</span>
                    </div>
                </div>
            )}
        </div>
    )
}

