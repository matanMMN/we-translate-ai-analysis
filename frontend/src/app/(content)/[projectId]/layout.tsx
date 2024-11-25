import "@/app/globals.css"
import '@/app/(content)/[projectId]/editor/page.module.css'
import {ReactNode} from "react";
import {AuthGuard} from "@/lib/AuthGuard";
import {log} from "@/lib/log";
import ProjectNavBar from "@/components/project/ProjectNavBar";
import ProjectProvider from "@/components/ProjectProvider";
import {fetchProjectById} from "@/actions/getUserProjects";


export default async function ProjectLayout(
    {
        children,
        params
    }: {
        children: ReactNode,
        params: Promise<{ projectId: string }>
    }): Promise<ReactNode> {

    await AuthGuard()

    log("Rendering specific project layout");

    const {projectId} = await params;
    const project = await fetchProjectById(projectId);
    if (!project) {
        return <div>Project not found</div>;
    }


    return (
        <ProjectProvider projectId={projectId} initialProject={project}>
            <div className="pb-8">
                <ProjectNavBar project={project}/>
                {children}
            </div>
        </ProjectProvider>
    );
}