import ProjectTable from "@/components/home/ProjectTable";
import {fetchProjects} from "@/actions/getUserProjects";

export const dynamic = 'force-dynamic'
export default async function HomePage() {
    const projects = await fetchProjects();

    return (
        <div className="flex text-lg">
            <div className="flex-1 flex flex-col overflow-hidden">
                <ProjectTable projects={projects}/>
            </div>
        </div>
    );
}
