import {Divider, List} from "@mui/material";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import SettingsIcon from "@mui/icons-material/Settings";
import React from "react";
import RouterLink from "@/components/drawer/RouterLink";
import Logout from "@/components/drawer/Logout";

export default function StaticMenu() {


    return (
        <nav className="px-2">
            <Divider/>
            <List>
                <RouterLink primary={"Help Center"} url={"help"} icon={<HelpOutlineIcon/>}/>
                <RouterLink primary={"About"} url={"about"} icon={<InfoOutlinedIcon/>}/>
                <Logout/>
                <RouterLink primary={"Settings"} url={"settings"} icon={<SettingsIcon/>}/>
            </List>
        </nav>
    )
}