import ProjectTable from "@/components/home/ProjectTable";


export default function Home() {

    return (
        <div className="flex text-lg">
            <div className="flex-1 flex flex-col overflow-hidden">
                {/*<NewProjectButton/>*/}
                <ProjectTable/>
            </div>
        </div>
    )
}