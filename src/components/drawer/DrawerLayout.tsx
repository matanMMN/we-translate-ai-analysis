import {ReactNode} from "react";
import LeftDrawer from "@/components/drawer/LeftDrawer";

export default async function DrawerLayout(): Promise<ReactNode> {
    // const projects: Array<Project> = await getUserProjects()
    // return projects && <LeftDrawer/>
    return <LeftDrawer/>
}