import "@/app/globals.css"
import '@/app/(content)/[projectId]/editor/page.module.css'
import {ReactNode} from "react";
import {AuthGuard} from "@/lib/AuthGuard";
import {redirect} from "next/navigation";
import {log} from "@/lib/log";
import ProjectNavBar from "@/components/project/ProjectNavBar";
import ProjectProvider from "@/components/ProjectProvider";
import {getUserProject} from "@/actions/getUserProjects";


export default async function ProjectLayout(
    {
        children,
        params
    }: {
        children: ReactNode,
        params: { projectId: string }
    }): Promise<ReactNode> {

    if (!await AuthGuard())
        return redirect('/login')

    log("Rendering specific project layout");

    const {projectId} = await params;
    const project = await getUserProject(projectId);

    if (!project) {
        return <div>Project not found</div>;
    }

    return (
        <ProjectProvider projectId={projectId} initialProject={project}>
            <div>
                <ProjectNavBar project={project}/>
                {children}
            </div>
        </ProjectProvider>
    );
}