'use client'

import {Card, CardContent} from "@/components/ui/card";
import {Badge} from "@/components/ui/badge";
import {Button} from "@/components/ui/button";
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select";
import {Calendar} from "@/components/ui/calendar";
import {Popover, PopoverContent, PopoverTrigger} from "@/components/ui/popover";
import {format} from "date-fns";
import {CalendarIcon} from "lucide-react";
import {getPriority, getPriorityColor, getStatusColor, getLanguage, getStatus} from "@/lib/functions";
import {InfoField} from "../components/InfoField";
import {Project} from "@/lib/userData";
import {useState} from "react";

interface ProjectInfoProps {
    project: Project;
    editProject: Project | null;
    isEditing: boolean;
    onEditAction: () => void;
    onSaveAction: () => void;
    onCancelAction: () => void;
    onChangeAction: (fields: Partial<Project>) => void;
}

export default function ProjectInfo({
                                        project,
                                        editProject,
                                        isEditing,
                                        onEditAction,
                                        onSaveAction,
                                        onCancelAction,
                                        onChangeAction
                                    }: ProjectInfoProps) {
    const [isCalendarOpen, setIsCalendarOpen] = useState(false)

    const renderEditableField = (field: any) => {
        switch (field.label) {
            case "Status":
                return (
                    <Select
                        value={editProject?.status || project.status}
                        onValueChange={(value) => onChangeAction({status: value})}
                    >
                        <SelectTrigger>
                            <SelectValue placeholder="Select status"/>
                        </SelectTrigger>
                        <SelectContent>
                            {["On Hold", "initial", "Planned", "Completed"].map((status) => (
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
                        value={editProject?.priority as string ?? project.priority as string}
                        onValueChange={(value) => onChangeAction({priority: value})}
                    >
                        <SelectTrigger>
                            <SelectValue placeholder="Select priority"/>
                        </SelectTrigger>
                        <SelectContent>
                            {[0, 1, 2, 3].map((priority) => (
                                <SelectItem key={priority} value={priority as unknown as string}>
                                    {getPriority(priority)}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                );
            case "Due date":
                return (
                    <Popover open={isCalendarOpen} onOpenChange={setIsCalendarOpen}>
                        <PopoverTrigger asChild>
                            <Button variant="outline"
                                    className="w-full lg:justify-start justify-center text-left font-normal">
                                <CalendarIcon className="lg:mr-2 h-4 w-4"/>
                                <div className="hidden lg:block">
                                    {editProject?.due_date ? format(new Date(editProject?.due_date), 'PPP') : project.due_date ? format(new Date(project.due_date), 'PPP') :
                                        <span>Pick a date</span>}
                                </div>
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-auto p-0">
                            <Calendar
                                mode="single"
                                selected={editProject?.due_date ? new Date(editProject?.due_date) : project.due_date ? new Date(project.due_date) : undefined}
                                onSelect={(date) => {
                                    if (date) {
                                        onChangeAction({due_date: date!.toISOString()})
                                        setIsCalendarOpen(false)
                                    }
                                }}
                                disabled={(date) => date < new Date()}
                                initialFocus
                            />
                        </PopoverContent>
                    </Popover>
                );
            default:
                return <InfoField {...field} />;
        }
    };
    const infoFields = [
        {label: "Name", value: project.title},
        {
            label: "Status",
            value: getStatus(editProject?.status || project!.status),
            className: getStatusColor(editProject?.status || project!.status)
        },
        {
            label: "Priority",
            value: editProject?.priority || project!.priority,
            render: (value: string) => (
                <Badge variant="secondary" className={getPriorityColor(value)}>
                    {getPriority(value)}
                </Badge>
            )
        },
        {label: "Last Update", value: project.updated_at?.toLocaleString()},
        {label: "Source Language", value: getLanguage(project.source_language)},
        {label: "Target Language", value: getLanguage(project.target_language)},
        {
            label: "Due date",
            value: new Date(editProject!.due_date!).toLocaleDateString("en") || new Date(project!.due_date!).toLocaleDateString("en")
        },
        {label: "Start date", value: project.created_at.toLocaleString()}
    ];
    return (
        <Card>
            <CardContent className="pt-6">
                <div className="flex justify-between items-center mb-4">
                    <h2 className="text-lg font-semibold">Project Details</h2>
                    <div className="space-x-2">
                        {isEditing ? (
                            <>
                                <Button
                                    onClick={onCancelAction}
                                    variant="outline"
                                >
                                    Cancel
                                </Button>
                                <Button
                                    onClick={onSaveAction}
                                    className="text-white"
                                >
                                    {"Save changes"}
                                </Button>
                            </>
                        ) : (
                            <Button
                                onClick={onEditAction}
                                variant="outline">
                                Edit Project details
                            </Button>
                        )}
                    </div>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                    {infoFields.map((field: any) => (
                        <div key={field.label}>
                            <div>
                                <div className="text-sm text-muted-foreground mb-1">{field.label}</div>
                                {isEditing && ["Status", "Priority", "Due date"].includes(field.label)
                                    ? renderEditableField(field) : <InfoField {...field} />
                                }
                            </div>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    )
        ;
}