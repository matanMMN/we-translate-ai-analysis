import {Divider, List} from "@mui/material";
import {CircleHelp, Info} from 'lucide-react'
import React from "react";
import RouterLink from "@/components/drawer/RouterLink";
import Logout from "@/components/drawer/Logout";
import {SettingsIcon} from "lucide-react";

export default function StaticMenu() {


    return (
        <nav className="px-2">
            <Divider/>
            <List>
                <RouterLink primary={"Help Center"} url={"help"} icon={<CircleHelp/>}/>
                <RouterLink primary={"About"} url={"about"} icon={<Info/>}/>
                <Logout/>
                <RouterLink primary={"Settings"} url={"settings"} icon={<SettingsIcon/>}/>
            </List>
        </nav>
    )
}