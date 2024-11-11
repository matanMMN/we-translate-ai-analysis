"use client"

import {SessionProvider} from "next-auth/react";
import React, {useEffect} from "react";

export default function AuthProviders({children}: Readonly<{ children: React.ReactNode }>) {
    const [isMobile, setIsMobile] = React.useState(false);
    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth <= 768);
        };

        handleResize();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    if (isMobile) {
        return <div
            className="w-full h-dvh flex font-bold text-center whitespace-pre-line justify-center items-center content-center">
            {`Mobile support is under development.
             For now please use your PC instead.`}</div>;
    }
    return (
        <SessionProvider>{children}</SessionProvider>
    );
}