import { ReactNode } from "react";
import { AuthGuard } from "@/lib/AuthGuard";
import Footer from "@/components/footer/Footer"
import LeftDrawer from "@/components/drawer/LeftDrawer";
import HeaderLayout from "@/components/header/HeaderLayout";
import DrawerProvider from "@/components/drawer/DrawerProvider";
import { log } from "@/lib/log";
import "@/app/globals.css"


export default async function RootLayout(
    {
        children, modal
    }: {
        children: ReactNode,
        modal: ReactNode
    }): Promise<ReactNode> {

    await AuthGuard()
    log("Rendering Layout");

    return (

        <>
            <HeaderLayout />
            <DrawerProvider>
                <LeftDrawer />
                <div
                    className="transition-all overflow-auto h-dvh max-h-[calc(100dvh-140px)] duration-300 ease-in-out my-20 mb-40 pt-8 px-20 flex flex-1 w-full flex-col">
                    {children}
                </div>
            </DrawerProvider>
            <Footer />
            {modal}
        </>

    );
}