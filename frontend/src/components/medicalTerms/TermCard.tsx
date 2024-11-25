import { Card, CardContent } from "@/components/ui/card";

export interface MedicalTerm {
    id: string;
    hebrewText: string;
    englishText: string;
    description: string;
    createdAt: Date;
    updatedAt: Date;
}

interface TermCardProps {
    term: MedicalTerm;
    language: 'hebrew' | 'english';
}

export function TermCard({ term, language }: TermCardProps) {
    const isHebrew = language === 'hebrew';

    return (
        <Card className="h-full transition-transform hover:shadow-lg">
            <CardContent className="p-6">
                <h2
                    className={`text-xl font-semibold mb-2 ${
                        isHebrew ? 'text-right rtl' : 'text-left ltr'
                    }`}
                >
                    {isHebrew ? term.hebrewText : term.englishText}
                </h2>
                <p className="text-sm text-muted-foreground mb-4">
                    {isHebrew ? term.englishText : term.hebrewText}
                </p>
                <p className="text-sm">
                    {term.description}
                </p>
            </CardContent>
        </Card>
    );
}