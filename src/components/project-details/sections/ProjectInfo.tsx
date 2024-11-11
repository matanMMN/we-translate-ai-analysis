'use client'

import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { getPriorityColor, getStatusColor } from "@/lib/functions";
import { InfoField } from "../components/InfoField";
import { Project } from "@/lib/userData";

interface ProjectInfoProps {
    project: Project;
}

export default function ProjectInfo({ project }: ProjectInfoProps) {
    const infoFields: any = [
        { label: "Name", value: project.name },
        { 
            label: "Status", 
            value: project.status,
            className: getStatusColor(project.status)
        },
        { 
            label: "Priority",
            value: project.priority,
            render: (value: string) => (
                <Badge variant="secondary" className={getPriorityColor(value)}>
                    {value}
                </Badge>
            )
        },
        { label: "Last Update", value: project.updatedAt?.toLocaleString() },
        { label: "Source Language", value: project.sourceLanguage },
        { label: "Target Language", value: project.destinationLanguage },
        { label: "Due date", value: project.dueDate?.toLocaleString() },
        { label: "Start date", value: project.createdAt.toLocaleString() }
    ];

    return (
        <Card>
            <CardContent className="pt-6">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                    {infoFields.map((field: any) => (
                        <InfoField key={field.label} {...field} />
                    ))}
                </div>
            </CardContent>
        </Card>
    );
} 