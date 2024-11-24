import {Suspense} from 'react';
import {MedicalTerms} from '@/components/medicalTerms/MedicalTerms';
import {TermCardSkeleton} from '@/components/medicalTerms/TermCardSkeleton';

export default async function MedicalTermsPage() {


    return (
        <main className="max-w-7xl mx-auto p-6 flex flex-col max-h-[calc(dvh-180px)]">
            <h1 className="text-3xl font-bold mb-6">Medical Terms</h1>
            {/*<SearchHeader initialTerms={terms}/>*/}
            {/*<LanguageTabs/>*/}
            <div className="flex-1 overflow-auto">
                <Suspense
                    fallback={
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {Array.from({length: 9}).map((_, i) => (
                                <TermCardSkeleton key={i}/>
                            ))}
                        </div>
                    }
                >
                    <MedicalTerms/>
                </Suspense>
            </div>
        </main>
    );
}