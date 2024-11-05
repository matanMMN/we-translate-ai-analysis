"use client"

import React, {MouseEventHandler, ReactNode, memo} from "react";
import Link from "next/link";
import {ListItemIcon, ListItemText} from "@mui/material";
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
            <button
                className={`w-full justify-center items-center text-start hover:border-none border-none border-b-4 hover:rounded-md rounded-md inline-flex px-2 py-1 pl-2 ring-transparent ring-0 m-0 gap-0 ${primary !== "Log out" && path === '/' + url ? 'hover:bg-[#1D3B34]' : 'hover:bg-gray-200'} my-2 border rounded-2xl ${primary !== "Log out" && (path === '/' + url || (path === '/' + "new-project" && primary === "Home")) ? 'bg-[#1D3B34]' : 'bg-transparent'}`}>
                <ListItemIcon
                    className={`gap-0 m-0 p-0 ${primary !== "Log out" && (path === '/' + url || (path === '/' + "new-project" && primary === "Home")) ? 'text-white' : ''}`}>
                    {icon}
                </ListItemIcon>
                <ListItemText
                    className={`text-2xl ${primary !== "Log out" && (path === '/' + url || (path === '/' + "new-project" && primary === "Home")) ? 'text-white' : 'text-black'}`}
                    primary={primary}/>
            </button>
        </Link>
    )
}, (prevProps, nextProps) => {
    return prevProps.primary === nextProps.primary &&
        prevProps.url === nextProps.url &&
        prevProps.icon === nextProps.icon &&
        prevProps.onClick === nextProps.onClick;
})


export default RouterLink