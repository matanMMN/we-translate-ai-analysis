"use client";

import { ReactNode, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { ProjectState, selectSession, setSessionSlice } from "@/store/slices/projectSlice";
import { getUser } from "@/lib/AuthGuard";
import { useProjectCache } from "@/hooks/useProjectCache";
import { useProjectRevalidation } from "@/hooks/useProjectRevalidation";
import { Project } from "@/lib/userData";

interface ProjectProviderProps {
    children: ReactNode;
    projectId: string;
    initialProject: Project;
}

export default function ProjectProvider({ 
    children, 
    projectId, 
    initialProject 
}: ProjectProviderProps) {
    const dispatch = useDispatch();
    const session = useSelector(selectSession);
    const { getProjectFromCache } = useProjectCache();
    const { revalidateProject } = useProjectRevalidation(projectId);

    useEffect(() => {
        const initializeProject = async () => {
            try {
                const newDispatch: ProjectState = {
                    projectId: session.projectId,
                    userSession: session.userSession,
                    project: session.project || initialProject
                };
                let isDispatchNeeded = false;

                // Check if project needs updating
                if (projectId !== session.projectId) {
                    isDispatchNeeded = true;
                    // Try to get from cache first
                    const cachedProject = await getProjectFromCache(projectId);
                    newDispatch.project = cachedProject || initialProject;
                    newDispatch.projectId = projectId;
                }

                // Check if user session needs fetching
                if (!session.userSession) {
                    isDispatchNeeded = true;
                    newDispatch.userSession = await getUser();
                }

                if (isDispatchNeeded) {
                    dispatch(setSessionSlice(newDispatch));
                }
            } catch (error) {
                console.error('Error initializing project:', error);
                // You might want to trigger an error boundary here
                throw new Error('Failed to initialize project');
            }
        };

        initializeProject();

        // Set up periodic revalidation
        const revalidationInterval = setInterval(() => {
            revalidateProject().catch(console.error);
        }, 5 * 60 * 1000); // Revalidate every 5 minutes

        return () => clearInterval(revalidationInterval);
    }, [projectId, dispatch, session.projectId, session.userSession, initialProject, getProjectFromCache, revalidateProject]);

    // Add error boundary wrapper
    if (!session.userSession || !session.project) {
        return null;
    }

    return children;
}