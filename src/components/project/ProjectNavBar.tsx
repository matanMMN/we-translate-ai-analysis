"use client"
import * as React from 'react'
import {FileText} from 'lucide-react'
import Link from 'next/link'
import {usePathname} from 'next/navigation'

import {cn} from '@/lib/utils'
import {Button} from '@/components/ui/button'

export default function ProjectNavBar() {
    // const router = useRouter()
    const path = usePathname()
    const navItems = [
        {name: 'Project details', path: '/project/details'},
        {name: 'Editor', path: '/project/editor'},
        {name: 'Side by side', path: '/project/side-by-side'},
        {name: 'Translate file', path: '/project/translate-file'},
        {name: 'Reference file', path: '/project/reference-file'},
    ]

    return (
        <div className=" bg-background">
            <header className="border-b">
                <div className="container py-4">
                    <div className="flex items-center gap-2 mb-4">
                        <FileText className="h-5 w-5"/>
                        <h1 className="text-xl font-semibold">Fostimon</h1>
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