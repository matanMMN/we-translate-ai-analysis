import React from "react";
import HomeIcon from "@mui/icons-material/Home";
import RouterLink from "@/components/drawer/RouterLink";
import {log} from "@/lib/log";
import AssignmentIcon from "@mui/icons-material/Assignment";
import HugeIcon from "@/assets/HugeIcon";
import IndustriesMenu from "@/components/drawer/IndustriesMenu";

export default function MenuBar() {

    log("Rendering MenuBar");


    return (
        <nav className="px-2">
            <RouterLink primary={"Home"} url={""} icon={<HomeIcon className="mr-3"/>}/>
            <RouterLink primary={"My Activity"} url={"my-activity"} icon={<AssignmentIcon className="mr-3"/>}/>
            <RouterLink primary={"Medical Terms"} url={"medical-terms"} icon={<HugeIcon/>}/>
            <IndustriesMenu/>
        </nav>)


}