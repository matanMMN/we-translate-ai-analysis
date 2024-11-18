'use client';

import {useSearchParams} from 'next/navigation';
import {TermsListClient} from './TermsList';
import {TermsPagination} from './TermsPagination';
import type {MedicalTerm} from './TermCard';
import {useEffect, useState} from "react";

interface MedicalTermsProps {
    initialTerms: MedicalTerm[];
}

export function MedicalTerms({initialTerms}: MedicalTermsProps) {
    const searchParams = useSearchParams();
    const searchQuery = searchParams.get('search') ?? '';
    const [results, setResults] = useState<MedicalTerm[]>([]);

    useEffect(() => {
        if (searchQuery !== '') {
            setResults(initialTerms?.filter((initialTerm: MedicalTerm) =>
                initialTerm.englishText.toLowerCase().includes(searchQuery.toLowerCase())
            ));
        }
    }, [initialTerms, searchQuery]);

    return (
        <div>
            <TermsListClient
                terms={!!results.length ? results : initialTerms}
                language={searchParams.get('language') as 'hebrew' | 'english' ?? 'hebrew'}
            />
            <TermsPagination totalPages={Math.ceil(initialTerms.length / 9)}/>
        </div>
    );
}