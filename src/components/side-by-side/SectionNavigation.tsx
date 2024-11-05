'use client'

import { Button } from "@/components/ui/button";
import { Plus, Trash2 } from "lucide-react";
import { useAppDispatch } from "@/hooks/useAppDispatch";
import { useAppSelector } from "@/hooks/useAppSelector";
import {
    addSection, 
    deleteSection,
    selectActiveSection, 
    selectSections,
    updateSection 
} from "@/store/slices/sideBySideSlice";
import { toast } from "sonner";

export function SectionNavigation() {
    const dispatch = useAppDispatch();
    const sections = useAppSelector(selectSections);
    const activeSection = useAppSelector(selectActiveSection);

    const handleDeleteSection = (id: string) => {
        if (sections.length <= 1) {
            toast.error("Cannot delete the last section");
            return;
        }
        dispatch(deleteSection(id));
    };

    const handleSectionClick = (id: string) => {
        dispatch(updateSection({ id }));
    };

    return (
        <div className="w-12 border-r bg-background flex flex-col items-center py-4 space-y-2">
            {sections.map((section) => (
                <div key={section.id} className="relative group">
                    <Button
                        variant={activeSection === section.id ? "default" : "ghost"}
                        className="w-8 h-8 rounded-full"
                        onClick={() => handleSectionClick(section.id)}
                    >
                        {section.id}
                    </Button>
                    {sections.length > 1 && (
                        <Button
                            variant="ghost"
                            size="icon"
                            className="absolute -right-8 top-0 hidden group-hover:flex"
                            onClick={() => handleDeleteSection(section.id)}
                        >
                            <Trash2 className="h-4 w-4" />
                        </Button>
                    )}
                </div>
            ))}
            <Button
                variant="ghost"
                className="w-8 h-8 rounded-full mt-auto"
                onClick={() => dispatch(addSection())}
            >
                <Plus className="h-4 w-4" />
            </Button>
        </div>
    );
} 