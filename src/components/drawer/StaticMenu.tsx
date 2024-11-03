"use client"
import {useCallback} from "react";
import {Divider, List} from "@mui/material";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import ExitToAppIcon from "@mui/icons-material/ExitToApp";
import SettingsIcon from "@mui/icons-material/Settings";
import React from "react";
import {signOut} from "next-auth/react";
import RouterLink from "@/components/drawer/RouterLink";

export default function StaticMenu() {

    const handleSignOut = useCallback(async () => {
        await signOut()
    }, [])

    return (
        <nav className="px-2">
            <Divider/>
            <List>
                <RouterLink primary={"Help Center"} url={"help"} icon={<HelpOutlineIcon/>}/>
                <RouterLink primary={"About"} url={"about"} icon={<InfoOutlinedIcon/>}/>
                <RouterLink primary="Log out" url={""} icon={<ExitToAppIcon/>} onClick={handleSignOut}/>
                <RouterLink primary={"Settings"} url={"settings"} icon={<SettingsIcon/>}/>
            </List>
        </nav>
    )
}