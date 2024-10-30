import SearchBar from "@/components/home/SearchBar";
import NewProjectButton from "@/components/home/NewProjectButton";
import ProjectTable from "@/components/home/ProjectTable";


export default function Home() {


    return (
        <div className="flex bg-background">
            <div className="flex-1 flex flex-col overflow-hidden">
                <SearchBar/>
                <main className="flex-1 p-6 overflow-hidden">
                    {/*<NewProjectButton/>*/}
                    <ProjectTable/>
                </main>
            </div>
        </div>
    )
}