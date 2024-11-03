import {ReactNode} from "react";
import {AuthGuard} from "@/lib/AuthGuard";
import {redirect} from "next/navigation";
import {log} from "@/lib/log";
import ProjectNavBar from "@/components/project/ProjectNavBar";


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

    const { projectId } = await params
    return (
        <>
            <ProjectNavBar projectId={projectId}/>
            {children}
        </>
    );
}
