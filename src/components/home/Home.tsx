import ProjectTable from "@/components/home/ProjectTable";
import {fetchProjects} from "@/actions/getUserProjects";


export default async function Home() {


    const projects = await fetchProjects();

    return (
        <div className="flex text-lg">
            <div className="flex-1 flex flex-col overflow-hidden">
                {/*<NewProjectButton/>*/}
                <ProjectTable projects={projects}/>
            </div>
        </div>
    )
}