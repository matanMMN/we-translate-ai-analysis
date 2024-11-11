'use client'

import { Card, CardContent } from "@/components/ui/card";

interface ProjectDescriptionProps {
    description: string;
}

export default function ProjectDescription({ description }: ProjectDescriptionProps) {
    return (
        <Card>
            <CardContent className="pt-6">
                <h2 className="text-lg font-semibold mb-2">Description</h2>
                <p className="text-muted-foreground">
                    {description}
                </p>
            </CardContent>
        </Card>
    );
} 