"use client"

import {memo} from "react";
import Link from "next/link";
import {ListItemIcon, ListItemText} from "@mui/material";
import {usePathname} from "next/navigation";
import {RouterLinkProps} from "./types";
import {getButtonStyles, getIconStyles, getTextStyles} from "./styles";

const RouterLink = memo(function RouterLink({
                                                primary,
                                                url,
                                                icon,
                                                onClick
                                            }: RouterLinkProps) {
    const path = usePathname();
    const isLogout = primary === 'Log out';
    const isActive = !isLogout && (path === `/${url}` || (path === '/new-project' && primary === 'Home'))

    return (
        <Link
            onClick={onClick}
            href={`/${url}`}
            className="no-underline text-inherit"
        >
            <button
                className={getButtonStyles({isActive, isLogout})}
            >
                <ListItemIcon className={getIconStyles({isActive, isLogout})}>
                    {icon}
                </ListItemIcon>
                <ListItemText
                    className={getTextStyles({isActive, isLogout})}
                    primary={primary}
                />
            </button>
        </Link>
    );
}, arePropsEqual);

function arePropsEqual(prevProps: RouterLinkProps, nextProps: RouterLinkProps) {
    return prevProps.primary === nextProps.primary &&
        prevProps.url === nextProps.url &&
        prevProps.icon === nextProps.icon &&
        prevProps.onClick === nextProps.onClick;
}

export default RouterLink;