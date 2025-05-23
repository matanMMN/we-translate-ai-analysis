import type { Metadata } from "next";
import "@/app/globals.css";
import { ReactNode } from "react";
import { protectLogin } from "@/lib/AuthGuard";
import { Grid } from "@mui/material";
// import Test from "@/components/testui";

export const metadata: Metadata = {
    title: "MediTranslate AI",
};

export interface ChildrenProps {
    children: ReactNode;
    logo: ReactNode
}

export default async function RootAuthLayout({ children, logo }: ChildrenProps): Promise<ReactNode> {

    await protectLogin();

    return (

        <Grid container component="main" sx={{ height: '100vh' }}>
            {/* <Test/> */}
            {logo}
            {children}
        </Grid>

    );
}
