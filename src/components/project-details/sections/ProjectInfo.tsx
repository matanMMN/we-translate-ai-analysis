'use client'

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { format } from "date-fns";
import { CalendarIcon } from "lucide-react";
import { getPriority, getPriorityColor, getStatusColor, getLanguage, getStatus } from "@/lib/functions";
import { InfoField } from "../components/InfoField";
import { Project } from "@/lib/userData";
import { useDispatch } from "react-redux";
import { updateProject } from "@/store/slices/sessionSlice";

interface ProjectInfoProps {
    project: Project;
}

export default function ProjectInfo({project}: ProjectInfoProps) {
    const [isEditing, setIsEditing] = useState(false);
    const [editedProject, setEditedProject] = useState(project);
    const dispatch = useDispatch();

    const handleSave = async () => {
        try {
            const response = await fetch(`http://localhost:8000/${project.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(editedProject),
            });

            if (!response.ok) throw new Error('Failed to update project');
            
            // Optimistically update the UI
            dispatch(updateProject(editedProject));
            setIsEditing(false);
        } catch (error) {
            console.error('Error updating project:', error);
            // You might want to add error handling UI here
        }
    };

    const renderEditableField = (field: any) => {
        switch (field.label) {
            case "Status":
                return (
                    <Select
                        value={editedProject.status}
                        onValueChange={(value) => setEditedProject({...editedProject, status: value})}
                    >
                        <SelectTrigger>
                            <SelectValue placeholder="Select status" />
                        </SelectTrigger>
                        <SelectContent>
                            {["not_started", "in_progress", "completed"].map((status) => (
                                <SelectItem key={status} value={status}>
                                    {getStatus(status)}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                );
            case "Priority":
                return (
                    <Select
                        value={editedProject.priority}
                        onValueChange={(value) => setEditedProject({...editedProject, priority: value})}
                    >
                        <SelectTrigger>
                            <SelectValue placeholder="Select priority" />
                        </SelectTrigger>
                        <SelectContent>
                            {["low", "medium", "high"].map((priority) => (
                                <SelectItem key={priority} value={priority}>
                                    {getPriority(priority)}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                );
            case "Due date":
                return (
                    <Popover>
                        <PopoverTrigger asChild>
                            <Button variant="outline" className="w-full justify-start text-left font-normal">
                                <CalendarIcon className="mr-2 h-4 w-4" />
                                {editedProject.dueDate ? format(new Date(editedProject.dueDate), 'PPP') : <span>Pick a date</span>}
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0">
                            <Calendar
                                mode="single"
                                selected={editedProject.dueDate ? new Date(editedProject.dueDate) : undefined}
                                onSelect={(date) => setEditedProject({...editedProject, dueDate: date})}
                                disabled={(date) => date < new Date()}
                            />
                        </PopoverContent>
                    </Popover>
                );
            default:
                return <InfoField {...field} />;
        }
    };

    const infoFields: any = [
        {label: "Name", value: project.title},
        {
            label: "Status",
            value: getStatus(project.status as string),
            className: getStatusColor(project.status)
        },
        {
            label: "Priority",
            value: project.priority,
            render: (value: string) => (
                <Badge variant="secondary" className={getPriorityColor(value)}>
                    {getPriority(value)}
                </Badge>
            )
        },
        {label: "Last Update", value: project.updatedAt?.toLocaleString()},
        {label: "Source Language", value: getLanguage(project.source_language)},
        {label: "Target Language", value: getLanguage(project.target_language)},
        {label: "Due date", value: project.dueDate?.toLocaleString()},
        {label: "Start date", value: project.createdAt.toLocaleString()}
    ];

    return (
        <Card>
            <CardContent className="pt-6">
                <div className="flex justify-between items-center mb-4">
                    <h2 className="text-lg font-semibold">Project Details</h2>
                    <Button
                        onClick={() => isEditing ? handleSave() : setIsEditing(true)}
                        variant="outline"
                    >
                        {isEditing ? "Save changes" : "Edit Project details"}
                    </Button>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                    {infoFields.map((field: any) => (
                        <div key={field.label}>
                            {isEditing && ["Status", "Priority", "Due date"].includes(field.label)
                                ? renderEditableField(field)
                                : <InfoField {...field} />
                            }
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
} 