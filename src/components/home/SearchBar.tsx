"use client"
import {Search} from "lucide-react";
import {Input} from "@/components/ui/input";
import {AnimatePresence, motion} from "framer-motion";
import {useState, useEffect} from "react";
import {useDebounce} from "use-debounce";

const projects = ['Fostimon', 'Fluoxetine', 'Finasteride', 'Fluconazole']


export default function SearchBar() {

    const [searchQuery, setSearchQuery] = useState('')
    const [debouncedQuery] = useDebounce(searchQuery, 300)
    const [searchResults, setSearchResults] = useState<string[]>([])
    const [showResults, setShowResults] = useState(false)

    useEffect(() => {
        if (debouncedQuery) {
            const results = projects.filter(term =>
                term.toLowerCase().includes(debouncedQuery.toLowerCase())
            )
            setSearchResults(results)
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
            className="border-b p-4 flex w-full justify-center relative"
        >
            <div className="relative bg-[#F0F2F5] border-none rounded-2xl">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground"/>
                <Input
                    placeholder="Search Project"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-9 h-[46px] w-[888px] focus:outline-none focus:ring-0 focus:border-blue-500"
                />
                <AnimatePresence>
                    {showResults && searchResults.length > 0 && (
                        <motion.div
                            initial={{opacity: 0, y: -10}}
                            animate={{opacity: 1, y: 0}}
                            exit={{opacity: 0, y: -10}}
                            className="absolute w-full mt-1 bg-background border rounded-md shadow-lg z-50"
                        >
                            {searchResults.map((result) => (
                                <motion.div
                                    key={result}
                                    initial={{opacity: 0}}
                                    animate={{opacity: 1}}
                                    exit={{opacity: 0}}
                                    className="px-4 py-2 hover:bg-muted cursor-pointer bg-[#98A7A3]"
                                    onClick={() => {
                                        setSearchQuery(result)
                                        setShowResults(false)
                                    }}
                                >
                                    <span className="font-normal">{result.slice(0, searchQuery.length)}</span>
                                    <span className="text-white font-normal">{result.slice(searchQuery.length)}</span>
                                </motion.div>
                            ))}
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </motion.header>
    )
}