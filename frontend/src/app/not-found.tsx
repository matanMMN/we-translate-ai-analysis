"use client"
import Link from "next/link";
import {ReactNode} from "react";
import "./globals.css"

export default function NotFound(): ReactNode {
    return (

        <div
            className="flex flex-col w-full h-dvh max-h-[50dvh] text-center items-center content-center justify-center">
            <h1 className="whitespace-pre-line text-5xl font-bold my-12">{`
             404 Oops!
             You seem to be lost.`}</h1>
            <Link className="underline text-2xl" href='/'>Home</Link>
        </div>
    )
}
