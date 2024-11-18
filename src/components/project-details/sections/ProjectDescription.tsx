'use client'

import { Card, CardContent } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

interface ProjectDescriptionProps {
    description: string;
    isEditing?: boolean;
    onDescriptionChange?: (value: string) => void;
}

export default function ProjectDescription({ description, isEditing = false, onDescriptionChange }: ProjectDescriptionProps) {
    return (
        <Card>
            <CardContent className="pt-6">
                <h2 className="text-lg font-semibold mb-2">Description</h2>
                {isEditing ? (
                    <Textarea
                        value={description}
                        onChange={(e) => onDescriptionChange?.(e.target.value)}
                        className="min-h-[100px]"
                    />
                ) : (
                    <p className="text-muted-foreground">
                        {description}
                    </p>
                )}
            </CardContent>
        </Card>
    );
} 