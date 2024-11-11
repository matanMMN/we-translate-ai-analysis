"use client"
import * as React from 'react'
import {FileText} from 'lucide-react'
import Link from 'next/link'
import {usePathname} from 'next/navigation'
import {cn} from '@/lib/utils'
import {Button} from '@/components/ui/button'

import {Project} from "@/lib/userData";

export default function ProjectNavBar({project}: { project: Project }) {

    const path = usePathname()
    const {id: projectId} = project
    const navItems = [
        {name: 'Project details', path: `/${projectId}/details`},
        {name: 'Editor', path: `/${projectId}/editor`},
        {name: 'Side by side', path: `/${projectId}/side-by-side`},
        {name: 'Translate file', path: `/${projectId}/translate-file`},
        {name: 'Reference file', path: `/${projectId}/reference-file`},
    ]

    return (

        <div className=" bg-background">
            <header className="border-b">
                <div className="container py-4">
                    <div className="flex flex-wrap items-center gap-2 mb-4">
                        <FileText className="h-5 w-5"/>
                        <h1 className="text-xl font-semibold">{project.name}</h1>
                    </div>

                    <nav className="flex space-x-2">
                        {navItems.map((item) => (
                            <Link key={item.path} href={item.path} passHref>
                                <Button
                                    variant={path === item.path ? 'default' : 'ghost'}
                                    className={cn(
                                        path === item.path && 'bg-[#1D3B34] text-white hover:bg-[#1D3B34]/90'
                                    )}
                                >
                                    {item.name}
                                </Button>
                            </Link>
                        ))}
                    </nav>
                </div>
            </header>
        </div>
    )
}