'use client'

import {useEffect} from 'react';
import {ThumbsUp, ThumbsDown} from 'lucide-react';
import {Button} from '@/components/ui/button';
import {LanguageSelector} from './LanguageSelector';
import {QuillEditor} from './QuillEditor';
import {GlossaryModal} from './GlossaryModal';
import {SectionNavigation} from './SectionNavigation';
import {useSections} from '@/hooks/useSections';
import {useAppDispatch} from '@/hooks/useAppDispatch';
import {useAppSelector} from '@/hooks/useAppSelector';
import {
    selectActiveSectionData, selectSections,
    selectSourceLanguage,
    selectTargetLanguage,
    updateSection
} from '@/store/slices/sideBySideSlice';
import {translateText} from '@/services/translationService';
import {useState} from 'react';
import {toast} from 'sonner';
import {useParams} from 'next/navigation';
import LoadingSpinner from "@/components/LoadingSpinner";


export default function SideBySide() {
    const params = useParams();
    const projectId = params.projectId as string;

    const sidebysideSlice = useAppSelector(state => state.sideBySide)
    console.log(sidebysideSlice)

    const dispatch = useAppDispatch();
    // const {isLoading, error} = useSections();
    const activeSection = useAppSelector(selectActiveSectionData)
    const sourceLang = useAppSelector(selectSourceLanguage);
    const targetLang = useAppSelector(selectTargetLanguage);
    const [isGlossaryOpen, setIsGlossaryOpen] = useState(false);
    const [isTranslating, setIsTranslating] = useState(false);


    console.log(activeSection)
    // useEffect(() => {
    //     if (error) {
    //         toast.error('Failed to load sections');
    //     }
    // }, [error]);

    const handleTranslate = async () => {
        if (!activeSection?.sourceContent) {
            toast.error('Please enter source text first');
            return;
        }

        if (!sourceLang) {
            toast.error('Source language not detected');
            return;
        }

        setIsTranslating(true);
        try {
            const result = await translateText({
                text: activeSection.sourceContent,
                sourceLang,
                targetLang,
                projectId
            });

            dispatch(updateSection({
                id: activeSection.id,
                targetContent: result.translatedText
            }));

            toast.success('Translation completed!');
        } catch (error) {
            console.error('Translation failed:', error);
            toast.error('Translation failed. Please try again.');
        } finally {
            setIsTranslating(false);
        }
    };

    // if (isLoading) {
    //     return (
    //         <div className="flex items-center justify-center h-[calc(100vh-300px)]">
    //             <LoadingSpinner/>
    //         </div>
    //     );
    // }

    if (!activeSection) {
        return (
            <div className="flex items-center justify-center h-[calc(100vh-300px)]">
                <p className="text-gray-500">No sections available. Copy text from the editor to get started.</p>
            </div>
        );
    }
    return (
        <div className="flex h-[calc(100vh-300px)]">
            <SectionNavigation/>

            <div className="flex-1 flex flex-col p-4">
                <LanguageSelector sourceLanguage={sourceLang || ''}/>

                <div className="grid grid-cols-2 gap-4 flex-1">
                    <QuillEditor
                        id={activeSection.id}
                        content={activeSection.sourceContent}
                        isRTL={sourceLang === 'he'}
                        readOnly={true} // Source content is read-only as it comes from the editor
                    />
                    {/*<QuillEditor*/}
                    {/*    id={activeSection.id}*/}
                    {/*    content={activeSection.targetContent}*/}
                    {/*    readOnly={false} // Target content is editable for translation*/}
                    {/*    isRTL={true} // Hebrew is always RTL*/}
                    {/*/>*/}
                </div>

                <div className="flex justify-between items-center mt-4">
                    <div className="flex gap-2">
                        <Button variant="ghost" size="icon" className="rounded-full">
                            <ThumbsUp className="h-4 w-4"/>
                        </Button>
                        <Button variant="ghost" size="icon" className="rounded-full">
                            <ThumbsDown className="h-4 w-4"/>
                        </Button>
                    </div>
                    <div className="flex gap-2">
                        <Button
                            className="bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white px-8"
                            onClick={handleTranslate}
                            disabled={isTranslating || !sourceLang}
                        >
                            {isTranslating ? 'Translating...' : 'Translate'}
                        </Button>
                        <Button
                            variant="secondary"
                            onClick={() => setIsGlossaryOpen(true)}
                        >
                            Glossary
                        </Button>
                    </div>
                </div>
            </div>

            <GlossaryModal
                open={isGlossaryOpen}
                onOpenChange={setIsGlossaryOpen}
                sourceLang={sourceLang || ''}
                targetLang={targetLang}
                projectId={projectId}
            />
        </div>
    );
}