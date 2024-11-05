'use client'

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { useAppDispatch } from "@/hooks/useAppDispatch";
import {useAppSelector} from "@/hooks/useAppSelector"
import { selectTargetLanguage, setTargetLanguage } from "@/store/slices/sideBySideSlice";

interface LanguageSelectorProps {
    sourceLanguage: string;
}

export function LanguageSelector({ sourceLanguage }: LanguageSelectorProps) {
    const dispatch = useAppDispatch();
    const targetLanguage = useAppSelector(selectTargetLanguage);

    const getLanguageLabel = (code: string) => {
        const languages = {
            'en': 'English',
            'he': 'Hebrew',
            // Add more languages as needed
        };
        return languages[code as keyof typeof languages] || code;
    };

    return (
        <div className="grid grid-cols-2 gap-4 mb-4">
            {/* Source language is always disabled as it comes from the editor */}
            <Select value={sourceLanguage} disabled>
                <SelectTrigger className="bg-gray-50">
                    <SelectValue placeholder="Source language">
                        {sourceLanguage ? getLanguageLabel(sourceLanguage) : 'Select language'}
                    </SelectValue>
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="en">English</SelectItem>
                    <SelectItem value="he">Hebrew</SelectItem>
                </SelectContent>
            </Select>

            {/* Target language is selectable */}
            <Select 
                value={targetLanguage} 
                onValueChange={(value) => dispatch(setTargetLanguage(value))}
            >
                <SelectTrigger className="bg-gray-50">
                    <SelectValue placeholder="Target language" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="he">Hebrew</SelectItem>
                    <SelectItem value="en">English</SelectItem>
                </SelectContent>
            </Select>
        </div>
    );
}