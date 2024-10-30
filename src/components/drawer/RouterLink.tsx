"use client"

import React, {MouseEventHandler, ReactNode, memo} from "react";
import Link from "next/link";
import {ListItemButton, ListItemIcon, ListItemText} from "@mui/material";
import {usePathname} from "next/navigation";

const RouterLink = memo(function RouterLink({primary, url, icon, onClick}: {
    primary: string,
    url: string,
    icon: ReactNode,
    onClick?: MouseEventHandler<HTMLAnchorElement> | undefined
}): ReactNode {

    const path = usePathname();

    return (
        <Link onClick={onClick && onClick} href={`/${url}`} className=" no-underline text-inherit">
            <ListItemButton
                className={`${primary !== "Log out" && path === '/' + url ? 'hover:bg-[#1D3B34]' : 'hover:bg-gray-200'} mx-2 my-2 border rounded-2xl ${primary !== "Log out" && (path === '/' + url || (path === '/' + "new-project" && primary === "Home")) && 'bg-[#1D3B34]'}`}>
                <ListItemIcon
                    className={`${primary !== "Log out" && (path === '/' + url || (path === '/' + "new-project" && primary === "Home")) ? 'text-white' : ''}`}>
                    {icon}
                </ListItemIcon>
                <ListItemText
                    className={`text-2xl ${primary !== "Log out" && (path === '/' + url || (path === '/' + "new-project" && primary === "Home")) ? 'text-white' : 'text-black'}`}
                    primary={primary}/>
            </ListItemButton>
        </Link>
    )
}, (prevProps, nextProps) => {
    return prevProps.primary === nextProps.primary &&
        prevProps.url === nextProps.url &&
        prevProps.icon === nextProps.icon &&
        prevProps.onClick === nextProps.onClick;
})


export default RouterLink