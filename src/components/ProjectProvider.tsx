"use client";
import {ReactNode, useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {ProjectState, selectSession, setSessionSlice, setUserSession} from "@/store/slices/projectSlice";
import {getUser} from "@/lib/AuthGuard";
import {getUserProject} from "@/actions/getUserProjects";

interface ProjectProviderProps {
    children: ReactNode;
    projectId: string;
}

export default function ProjectProvider({children, projectId}: ProjectProviderProps) {
    const dispatch = useDispatch();
    const session = useSelector(selectSession);
    useEffect(() => {
        const fetchData = async () => {
            const newDispatch: ProjectState = {
                projectId: session.projectId,
                userSession: session.userSession,
                project: session.project
            }
            let isDispatchNeeded = false;

            if (projectId && !session.projectId) {
                console.log("project change detected")
                isDispatchNeeded = true;
                newDispatch.project = await getUserProject(projectId);
                newDispatch.projectId = projectId;
            }
            if (!session.userSession) {
                console.log("user change detected")
                isDispatchNeeded = true;
                newDispatch.userSession = await getUser();
            }
            if (isDispatchNeeded) {
                console.log("Dispatching new data")
                dispatch(setSessionSlice(newDispatch));
            }

        };

        fetchData();
    }, [projectId, dispatch, session]);

    return session.userSession && session.project && children
}