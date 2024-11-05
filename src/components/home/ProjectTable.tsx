"use client"
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table";
import {Badge} from "@/components/ui/badge";
import {cn} from "@/lib/utils";
import {getPriorityColor, getStatusColor} from "@/lib/functions";
import {DropdownMenu} from "@/components/ui/dropdown-menu";
import {Button} from "@/components/ui/button";
import {ChevronDown, ChevronUp, Edit2, Search} from "lucide-react";
import {AnimatePresence, motion} from "framer-motion";
import {useEffect, useMemo, useRef, useState} from "react";
import {useVirtualizer} from "@tanstack/react-virtual";
import {useDebounce} from "use-debounce";
import {Input} from "@/components/ui/input";
import Link from "next/link";
import {useSession} from "next-auth/react";
import LoadingLogoGif from "@/components/LoadingLogoGif";
import {Project} from "@/lib/userData";
import {useRouter} from "next/navigation";


// export interface Project {
//     id: string
//     project_name: string
//     priority: 'Low' | 'Normal' | 'High' | 'Critical'
//     status: 'Planned' | 'In Progress' | 'Completed' | 'On Hold'
// }

export type SortConfig = {
    key: keyof Project | null
    direction: 'asc' | 'desc'
}


export default function ProjectTable() {


    const {data: session, status} = useSession()
    const projects = session?.userData?.allProjects
    const router = useRouter()

    const [sortConfig, setSortConfig] = useState<SortConfig>({key: null, direction: 'asc'})
    const parentRef = useRef<HTMLDivElement>(null)
    const [searchQuery, setSearchQuery] = useState('')
    const [debouncedQuery] = useDebounce(searchQuery, 300)
    const [searchResults, setSearchResults] = useState<Project[]>([])
    const [showResults, setShowResults] = useState(false)

    useEffect(() => {
        if (debouncedQuery) {
            const results = projects?.filter(project =>
                project.name.toLowerCase().includes(debouncedQuery.toLowerCase())
            )
            setSearchResults(results ?? [])
            setShowResults(true)
        } else {
            setSearchResults([])
            setShowResults(false)
        }
    }, [debouncedQuery, projects])

    const sortedProjects = useMemo(() => {
        if (!sortConfig.key) return projects
        if (projects) {
            return [...projects].sort((a, b) => {
                if (a[sortConfig.key] <= b[sortConfig.key]) {
                    return sortConfig.direction === 'asc' ? -1 : 1
                }
                if (a[sortConfig.key] > b[sortConfig.key]) {
                    return sortConfig.direction === 'asc' ? 1 : -1
                }
                return 0
            })
        }
    }, [projects, sortConfig])

    const rowVirtualizer = useVirtualizer({
        count: searchResults.length > 0 ? searchResults.length : projects?.length ?? 0,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 60,
        overscan: 10,
    })





    const SortableHeader = ({column, width}: { column: keyof Project, width: string }) => {
        const isActive = sortConfig.key === column

        const handleSort = (key: keyof Project) => {
            setSortConfig(current => ({
                key,
                direction: current.key === key && current.direction === 'asc' ? 'desc' : 'asc'
            }))
        }


        return (
            <TableHead
                style={{width}}
                className="group cursor-pointer transition-colors hover:bg-muted/50 "
                onClick={() => handleSort(column)}
            >
                <div className="flex items-center gap-2">
                    <span className="text-2xl">{column.charAt(0).toUpperCase() + column.slice(1)}</span>
                    <div className="flex flex-col opacity-0 group-hover:opacity-100 transition-opacity">
                        <ChevronUp
                            className={cn(
                                "w-3 h-3 -mb-1",
                                isActive && sortConfig.direction === 'asc' ? "text-foreground" : "text-muted-foreground"
                            )}
                        />
                        <ChevronDown
                            className={cn(
                                "w-3 h-3",
                                isActive && sortConfig.direction === 'desc' ? "text-foreground" : "text-muted-foreground"
                            )}
                        />
                    </div>
                </div>
            </TableHead>
        )
    }
    return status === 'loading' ? <LoadingLogoGif/> : (
        <>
            <motion.header
                initial={{y: -20, opacity: 0}}
                animate={{y: 0, opacity: 1}}
                transition={{delay: 0.2}}
                className="p-4 flex w-full justify-center relative"
            >
                <div className="relative bg-[#F0F2F5] border-none rounded-2xl w-full max-w-2xl">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-6 h-6 text-muted-foreground"/>
                    <Input
                        placeholder="Search Project"
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
                                        key={result.name}
                                        initial={{opacity: 0}}
                                        animate={{opacity: 1}}
                                        exit={{opacity: 0}}
                                        className="px-4 py-2 transition-all duration-250 hover:bg-gray-300 cursor-pointer bg-[#98A7A3]"
                                        onClick={() => {
                                            setSearchQuery(result.name)
                                            setShowResults(false)
                                        }}
                                    >
                                        <span className="font-normal">{result.name.slice(0, searchQuery.length)}</span>
                                        <span
                                            className="text-white font-normal">{result.name.slice(searchQuery.length)}</span>
                                    </motion.div>
                                ))}
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </motion.header>

            <main className="flex-1 p-8 overflow-hidden">

                <motion.div
                    initial={{y: 40, opacity: 0}}
                    animate={{y: 0, opacity: 1}}
                    transition={{delay: 0.4}}
                    ref={parentRef}
                    className="border-2 border-gray-200 dark:border-gray-700 rounded-2xl overflow-auto h-[calc(100vh-20rem)] shadow-inner bg-white dark:bg-gray-800"
                >
                    <div className="min-w-[900px]">
                        <Table>
                            <TableHeader className="sticky top-0 bg-gray-50 dark:bg-gray-900 z-10">
                                <TableRow
                                    className="hover:bg-transparent">
                                    <SortableHeader column={`${'project Name' as "name"}`} width="30%"/>
                                    <SortableHeader column="priority" width="30%"/>
                                    <SortableHeader column="status" width="30%"/>
                                    <TableHead style={{width: '10%'}}
                                               className="text-lg font-semibold">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody style={{
                                height: `${rowVirtualizer.getTotalSize()}px`,
                                width: '100%',
                                position: 'relative',
                            }}>
                                {rowVirtualizer.getVirtualItems().map((virtualRow) => {
                                    let project
                                    if (searchResults.length > 0) {
                                        project = searchResults[virtualRow.index]
                                    } else {
                                        project = sortedProjects![virtualRow.index]
                                    }
                                    return (
                                        <TableRow
                                            key={project.id}
                                            className="absolute w-full flex items-center text-center hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                                            style={{
                                                height: `${virtualRow.size}px`,
                                                transform: `translateY(${virtualRow.start}px)`,
                                            }}
                                        >

                                            <TableCell onClick={() => router.push(`/${project.id}/details`)}
                                                       className="text-lg hover:cursor-pointer max-w-[30%] w-full text-start">{project.name}</TableCell>

                                            <TableCell style={{width: '30%'}}
                                                       className="py-6 text-start w-full max-w-[30%]">
                                                <Badge variant="secondary"
                                                       className={cn('text-base font-medium px-4 py-2 ', getPriorityColor(project.priority))}>
                                                    {project.priority}
                                                </Badge>
                                            </TableCell>
                                            <TableCell style={{width: '30%'}}
                                                       className="py-6 text-start w-full max-w-[30%]">
                                        <span className={cn('text-lg font-bold', getStatusColor(project.status))}>
                                          {project.status}
                                        </span>
                                            </TableCell>
                                            <TableCell style={{width: '10%'}}
                                                       className="py-6 text-start w-full max-w-[30%]">
                                                <DropdownMenu>
                                                    <Link href={`/${project.id}/details`}>
                                                        <Button variant="ghost" size="icon"
                                                                className="hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full w-12 h-12">
                                                            <Edit2 className="w-6 h-6"/>
                                                        </Button>
                                                    </Link>
                                                </DropdownMenu>
                                            </TableCell>
                                        </TableRow>
                                    )
                                })}
                            </TableBody>
                        </Table>
                    </div>
                </motion.div>
            </main>
        </>
    )
}