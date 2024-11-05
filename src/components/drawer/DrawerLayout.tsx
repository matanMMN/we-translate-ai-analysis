import {ReactNode} from "react";
import LeftDrawer from "@/components/drawer/LeftDrawer";

export default async function DrawerLayout(): Promise<ReactNode> {
    return <LeftDrawer/>
}