"use client"
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table";
import {Badge} from "@/components/ui/badge";
import {cn} from "@/lib/utils";
import {DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger} from "@/components/ui/dropdown-menu";
import {Button} from "@/components/ui/button";
import {ChevronDown, ChevronUp, Edit2} from "lucide-react";
import {motion} from "framer-motion";
import {useMemo, useRef, useState} from "react";
import {useVirtualizer} from "@tanstack/react-virtual";

export interface Project {
    id: string
    name: string
    priority: 'Low' | 'Normal' | 'High' | 'Critical'
    status: 'Planned' | 'In Progress' | 'Completed' | 'On Hold'
}

export type SortConfig = {
    key: keyof Project | null
    direction: 'asc' | 'desc'
}


export default function ProjectTable() {

    const projects: Project[] = useMemo(() =>
            Array.from({length: 20}, (_, i) => ({
                id: `project-${i}`,
                name: `Project ${i + 1}`,
                priority: ['Low', 'Normal', 'High', 'Critical'][Math.floor(Math.random() * 4)] as Project['priority'],
                status: ['Planned', 'In Progress', 'Completed', 'On Hold'][Math.floor(Math.random() * 4)] as Project['status'],
            }))
        , [])

    const [sortConfig, setSortConfig] = useState<SortConfig>({key: null, direction: 'asc'})
    const parentRef = useRef<HTMLDivElement>(null)

    const sortedProjects = useMemo(() => {
        if (!sortConfig.key) return projects

        return [...projects].sort((a, b) => {
            if (a[sortConfig.key!] <= b[sortConfig.key!]) {
                return sortConfig.direction === 'asc' ? -1 : 1
            }
            if (a[sortConfig.key!] > b[sortConfig.key!]) {
                return sortConfig.direction === 'asc' ? 1 : -1
            }
            return 0
        })
    }, [projects, sortConfig])

    const rowVirtualizer = useVirtualizer({
        count: sortedProjects.length,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 60,
        overscan: 10,
    })

    const getPriorityColor = (priority: Project['priority']) => {
        switch (priority) {
            case 'Low':
                return 'bg-emerald-500/10 text-emerald-500'
            case 'Normal':
                return 'bg-blue-500/10 text-blue-500'
            case 'High':
                return 'bg-amber-500/10 text-amber-500'
            case 'Critical':
                return 'bg-red-500/10 text-red-500'
        }
    }

    const getStatusColor = (status: Project['status']) => {
        switch (status) {
            case 'Planned':
                return 'text-slate-500'
            case 'In Progress':
                return 'text-blue-500'
            case 'Completed':
                return 'text-emerald-500'
            case 'On Hold':
                return 'text-amber-500'
        }
    }


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
                className="group cursor-pointer transition-colors hover:bg-muted/50"
                onClick={() => handleSort(column)}
            >
                <div className="flex items-center gap-2">
                    <span>{column.charAt(0).toUpperCase() + column.slice(1)}</span>
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

    return (
        <motion.div
            initial={{y: 40, opacity: 0}}
            animate={{y: 0, opacity: 1}}
            transition={{delay: 0.4}}
            ref={parentRef}
            className="border rounded-lg overflow-hidden h-[calc(100vh-20rem)]"
            style={{
                overflowY: 'auto',
                overflowX: 'hidden'
            }}
        >
            <div className="min-w-[800px]">
                <Table>
                    <TableHeader className="sticky top-0 bg-background z-10">
                        <TableRow className="hover:bg-transparent">
                            <SortableHeader column="name" width="30%"/>
                            <SortableHeader column="priority" width="30%"/>
                            <SortableHeader column="status" width="30%"/>
                            <TableHead style={{width: '10%'}}>Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody style={{
                        height: `${rowVirtualizer.getTotalSize()}px`,
                        width: '100%',
                        position: 'relative',
                    }}>
                        {rowVirtualizer.getVirtualItems().map((virtualRow) => {
                            const project = sortedProjects[virtualRow.index]
                            return (
                                <TableRow
                                    key={project.id}
                                    className="absolute w-full hover:bg-muted/50 transition-colors"
                                    style={{
                                        height: `${virtualRow.size}px`,
                                        transform: `translateY(${virtualRow.start}px)`,
                                    }}
                                >
                                    <TableCell
                                        className="py-4 w-[60rem]">{project.name}</TableCell>
                                    <TableCell style={{width: '30%'}} className="py-4">
                                        <Badge variant="secondary"
                                               className={cn('font-medium', getPriorityColor(project.priority))}>
                                            {project.priority}
                                        </Badge>
                                    </TableCell>
                                    <TableCell style={{width: '30%'}} className="py-4">
                            <span className={cn('font-medium', getStatusColor(project.status))}>
                              {project.status}
                            </span>
                                    </TableCell>
                                    <TableCell style={{width: '10%'}} className="py-4">
                                        <DropdownMenu>
                                            <DropdownMenuTrigger asChild>
                                                <Button variant="ghost" size="icon"
                                                        className="hover:scale-105 transition-transform">
                                                    <Edit2 className="w-4 h-4"/>
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent align="end">
                                                <DropdownMenuItem>Edit Project</DropdownMenuItem>
                                                <DropdownMenuItem>Change Priority</DropdownMenuItem>
                                                <DropdownMenuItem>Update Status</DropdownMenuItem>
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </TableCell>
                                </TableRow>
                            )
                        })}
                    </TableBody>
                </Table>
            </div>
        </motion.div>
    )
}