'use client';

import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useRouter, useSearchParams } from 'next/navigation';

export function LanguageTabs() {
    const router = useRouter();
    const searchParams = useSearchParams();

    const handleLanguageChange = (value: string) => {
        const params = new URLSearchParams(searchParams);
        params.set('language', value);
        params.set('page', '1');
        router.push(`/medical-terms?${params.toString()}`);
    };

    return (
        <Tabs
            defaultValue={searchParams.get('language') ?? 'hebrew'}
            onValueChange={handleLanguageChange}
            className="mb-6"
        >
            <TabsList>
                <TabsTrigger value="hebrew">Hebrew terms</TabsTrigger>
                <TabsTrigger value="english">English terms</TabsTrigger>
            </TabsList>
        </Tabs>
    );
}