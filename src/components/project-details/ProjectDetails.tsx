'use client'

import { useSelector } from "react-redux";
import { selectSession } from "@/store/slices/projectSlice";
import dynamic from 'next/dynamic';
import ProjectInfo from "./sections/ProjectInfo";
import ProjectDescription from "./sections/ProjectDescription";
import ProjectMembers from "./sections/ProjectMembers";
import ProjectActivity from "./sections/ProjectActivity";

const EditOrViewGrid = dynamic(
    () => import("@/components/editor/EditOrViewGrid"),
    {
        loading: () => <div className="h-20 animate-pulse bg-gray-200 rounded-md" />,
        ssr: false
    }
);

export default function ProjectDetails() {
    const { project, userSession } = useSelector(selectSession);

    if (!project) return null;

    return (
        <div className="space-y-8">
            <ProjectInfo project={project} />
            <ProjectDescription description={project.description} />
            {userSession && <EditOrViewGrid userSession={userSession} />}
            <div className="grid grid-cols-2 gap-8">
                <ProjectMembers members={project.members} />
                <ProjectActivity activities={project.activities} />
            </div>
        </div>
    );
}