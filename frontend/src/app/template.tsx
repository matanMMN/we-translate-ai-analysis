'use client'

import { usePathname } from 'next/navigation';
import { Suspense } from 'react';
import Loading from './loading';

export default function Template({ children }: { children: React.ReactNode }) {
    const pathname = usePathname();

    return (
        <Suspense key={pathname} fallback={<Loading />}>
            {children}
        </Suspense>
    );
} 