'use client'

import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import { 
    addSection, 
    selectActiveSection, 
    selectSections, 
    setActiveSection 
} from "@/store/slices/sideBySideSlice";

export function SectionNavigation() {
    const dispatch = useDispatch();
    const sections = useSelector(selectSections);
    const activeSection = useSelector(selectActiveSection);

    return (
        <div className="w-12 border-r bg-background flex flex-col items-center py-4 space-y-2">
            {sections.map((section) => (
                <Button
                    key={section.id}
                    variant={activeSection === section.id ? "default" : "ghost"}
                    className="w-8 h-8 rounded-full"
                    onClick={() => dispatch(setActiveSection(section.id))}
                >
                    {section.id}
                </Button>
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