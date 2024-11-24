import {ReactNode} from "react";
import localFont from "next/font/local";
import type {Metadata} from "next";
import "@/app/globals.css"
import {Toaster} from "sonner";


const geistSans = localFont({
    src: "./fonts/GeistVF.woff",
    variable: "--font-geist-sans",
    weight: "100 900",
});
const geistMono = localFont({
    src: "./fonts/GeistMonoVF.woff",
    variable: "--font-geist-mono",
    weight: "100 900",
});

export const metadata: Metadata = {
    title: "WeTranslate AI",
};

export interface ChildrenProps {
    children: ReactNode;
}

export default function DefaultLayout({children}: { children: ReactNode }) {


    return (
        <html lang="en">
        <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <Toaster/>
        {children}
        </body>
        </html>
    )
}