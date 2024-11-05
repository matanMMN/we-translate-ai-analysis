import {ReactNode} from "react";
import {StoreProvider} from "@/components/StoreProvider";
import AuthProviders from "@/components/AuthProviders";
import {AuthGuard} from "@/lib/AuthGuard";
import Footer from "@/components/footer/Footer"
import LeftDrawer from "@/components/drawer/LeftDrawer";
import HeaderLayout from "@/components/header/HeaderLayout";
import DrawerProvider from "@/components/drawer/DrawerProvider";
import {log} from "@/lib/log";
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
        <AuthProviders>
            <StoreProvider>
                <HeaderLayout/>
                <DrawerProvider>
                    <LeftDrawer/>
                    <div
                        className="transition-all duration-300 ease-in-out mt-14 pt-12 px-20 flex flex-1 w-full flex-col">
                        {children}
                    </div>
                </DrawerProvider>
                <Footer/>
                {modal}
            </StoreProvider>
        </AuthProviders>
    );
}