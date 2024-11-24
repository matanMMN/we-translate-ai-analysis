'use client';

import {Search} from 'lucide-react';
import {Input} from "@/components/ui/input";
import {AnimatePresence, motion} from 'framer-motion';
import {useEffect, useState} from 'react';
import {useDebounce} from "use-debounce";
import type {MedicalTerm} from './TermCard';
import {useRouter, useSearchParams} from "next/navigation";

interface SearchHeaderProps {
    initialTerms: MedicalTerm[];
}

export function SearchHeader({initialTerms}: SearchHeaderProps) {

    const router = useRouter()
    const searchParams = useSearchParams()
    const [searchQuery, setSearchQuery] = useState('');
    const [debouncedQuery] = useDebounce(searchQuery, 100)
    const [searchResults, setSearchResults] = useState<MedicalTerm[]>([]);
    const [showResults, setShowResults] = useState(false)

    useEffect(() => {
        if (debouncedQuery) {
            const results = initialTerms?.filter((initialTerm: MedicalTerm) =>
                initialTerm.englishText.toLowerCase().includes(debouncedQuery.toLowerCase())
            )
            const params = new URLSearchParams(searchParams);
            params.set('search', searchQuery);
            router.push(`/medical-terms?${params.toString()}`);
            setSearchResults(results ?? [])
            setShowResults(true)
        } else {
            setSearchResults([])
            setShowResults(false)
        }
    }, [debouncedQuery])

    return (
        <motion.header
            initial={{y: -20, opacity: 0}}
            animate={{y: 0, opacity: 1}}
            transition={{delay: 0.2}}
            className="p-4 pb-20 flex w-full justify-center relative"
        >
            <div className="relative bg-[#F0F2F5] border-none rounded-2xl w-full max-w-2xl">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-6 h-6 text-muted-foreground"/>
                <Input
                    placeholder="Search glossary terms"
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
                            {searchResults.map((result) => (
                                <motion.div
                                    key={result.id}
                                    initial={{opacity: 0}}
                                    animate={{opacity: 1}}
                                    exit={{opacity: 0}}
                                    className="px-4 py-2 transition-all duration-250 hover:bg-gray-300 cursor-pointer bg-[#98A7A3]"
                                    onClick={() => {
                                        setSearchQuery(result.englishText);
                                        setShowResults(false);
                                        const params = new URLSearchParams(searchParams);
                                        params.set('search', result.englishText);
                                        router.push(`/medical-terms?${params.toString()}`);
                                    }}
                                >
                                    {
                                        result.englishText.toLowerCase().indexOf(searchQuery.toLowerCase()) >= 0 &&

                                        <div className="flex items-center">
                                        <span
                                            className="font-normal text-white">{result.englishText.slice(0, result.englishText.toLowerCase().indexOf(searchQuery.toLowerCase()))}</span>
                                            <span
                                                className="font-normal">{result.englishText.slice(result.englishText.toLowerCase().indexOf(searchQuery.toLowerCase()), result.englishText.toLowerCase().indexOf(searchQuery.toLowerCase()) + searchQuery.length)}</span>
                                            <span
                                                className="font-normal text-white">{result.englishText.slice(result.englishText.toLowerCase().indexOf(searchQuery.toLowerCase()) + searchQuery.length)}</span>
                                        </div>
                                    }
                                    <div className="text-sm text-muted-foreground">
                                        {result.hebrewText}
                                    </div>
                                </motion.div>
                            ))}
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </motion.header>
    );
}