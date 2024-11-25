'use client';

import {MedicalTerm, TermCard} from './TermCard';

interface TermsListClientProps {
    terms: MedicalTerm[];
    language: 'hebrew' | 'english';
}

export function TermsListClient({ terms, language }: TermsListClientProps) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pb-6">
            {terms.map((term) => (
                <TermCard
                    key={term.id}
                    term={term}
                    language={language}
                />
            ))}
        </div>
    );
}