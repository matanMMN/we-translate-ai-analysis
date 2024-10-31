import type {Metadata} from "next";
import localFont from "next/font/local";
import "../globals.css";
import {ReactNode} from "react";
import {StoreProvider} from "@/components/StoreProvider";
import AuthProviders from "@/components/AuthProviders";
import {AuthGuard} from "@/lib/AuthGuard";
import Footer from "@/components/footer/Footer"
import {redirect} from "next/navigation";
import LeftDrawer from "@/components/drawer/LeftDrawer";
import HeaderLayout from "@/components/header/HeaderLayout";
import DrawerProvider from "@/components/drawer/DrawerProvider";
import {log} from "@/lib/log";

const geistSans = localFont({
    src: "../fonts/GeistVF.woff",
    variable: "--font-geist-sans",
    weight: "100 900",
});
const geistMono = localFont({
    src: "../fonts/GeistMonoVF.woff",
    variable: "--font-geist-mono",
    weight: "100 900",
});

export const metadata: Metadata = {
    title: "WeTranslate AI",
};

export interface ChildrenProps {
    children: ReactNode;
}

export default async function RootLayout(
    {
        children, modal
    }: {
        children: ReactNode,
        modal: ReactNode
    }): Promise<ReactNode> {

    if (!await AuthGuard())
        return redirect('/login')

    log("Rendering Layout");

    return (
        <html lang="en">
        <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <AuthProviders>
            <StoreProvider>
                <HeaderLayout/>
                <DrawerProvider>
                    <LeftDrawer/>
                    <div
                        className={`flex-1 flex flex-col pt-12 px-20 transition-all duration-300 ease-in-out`}>
                        {children}
                    </div>
                </DrawerProvider>
                <Footer/>
                {modal}
            </StoreProvider>
        </AuthProviders>
        </body>
        </html>
    );
}
