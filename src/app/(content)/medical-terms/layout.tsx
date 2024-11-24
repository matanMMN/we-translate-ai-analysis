import {ReactNode} from "react";

export const metadata = {
    title: 'Medical Terms Glossary',
    description: 'Browse medical terms in Hebrew and English',
};

export default function MedicalTermsLayout({children}: { children: ReactNode }): ReactNode {
    return (
        <>
            {children}
        </>
    )
}