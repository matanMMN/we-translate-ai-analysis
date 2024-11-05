import type {Metadata} from "next";
import "@/app/globals.css";
import {ReactNode} from "react";
import {StoreProvider} from "@/components/StoreProvider";
import AuthProviders from "@/components/AuthProviders";
import {protectLogin} from "@/lib/AuthGuard";


export const metadata: Metadata = {
    title: "WeTranslate AI",
};

export interface ChildrenProps {
    children: ReactNode;
}

export default async function RootAuthLayout({children}: ChildrenProps): Promise<ReactNode> {

    await protectLogin();

    return (
        <AuthProviders>
            <StoreProvider>
                {children}
            </StoreProvider>
        </AuthProviders>
    );
}
