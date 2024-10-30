import type {Metadata} from "next";
import "@/app/globals.css";
import {ReactNode} from "react";
import {StoreProvider} from "@/components/StoreProvider";
import AuthProviders from "@/components/AuthProviders";
import {AuthGuard} from "@/lib/AuthGuard";
import {redirect} from "next/navigation";


export const metadata: Metadata = {
    title: "WeTranslate AI",
};

export interface ChildrenProps {
    children: ReactNode;
}

export default async function RootAuthLayout({children}: ChildrenProps): Promise<ReactNode> {

    if (await AuthGuard())
        return redirect('/')

    return (
        <html lang="en">
        <body>
        <AuthProviders>
            <StoreProvider>
                {children}
            </StoreProvider>
        </AuthProviders>
        </body>
        </html>
    );
}
