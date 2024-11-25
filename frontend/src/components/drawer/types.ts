import { MouseEventHandler, ReactNode } from "react";

export interface RouterLinkProps {
    primary: string;
    url: string;
    icon: ReactNode;
    onClick?: MouseEventHandler<HTMLAnchorElement>;
}

export interface StyleProps {
    isActive: boolean;
    isLogout?: boolean;
} 