"use client"

import React, {ReactNode} from 'react';
import LoadingSpinner from '@/components/LoadingSpinner';
import {useSession} from "next-auth/react";
import {Button} from "@/components/ui/button";
import {Divider} from "@mui/material";
import {log} from "@/lib/log";
import Link from "next/link";
import {useRouter} from "next/navigation";


const UserProfilePanel = (): ReactNode => {

    const {data: session, status} = useSession()
    const router = useRouter()
    log(`Rendering User Profile Panel with User Data of: ${session?.userData!.first_name} ${session?.userData!.last_name}, loading status: ${status}`);

    return status === "loading" ? <LoadingSpinner/> : (
        <>
            <div
                className="flex flex-col max-w-[275px] max-h-[103px] items-center p-4 bg-[#1D3B34] mx-2 mb-2 border rounded-3xl">
                <div className="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center mr-3">
                    <span className="text-[#1a3937] font-semibold">
                        {session!.userData!.first_name![0] + session!.userData!.last_name[0]}
                    </span>
                </div>
                <span
                    className="font-semibold text-white">{`${session?.userData!.first_name} ${session?.userData!.last_name}`}</span>

                <Button className="mx-2 mb-2 bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white border rounded-2xl h-[45px]"
                        onClick={() => router.push('/new-project')}>
                    + New Project
                </Button>
            </div>

            <Button className="mx-2 mb-2 bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white border rounded-2xl h-[45px]"
                    onClick={() => router.push('/new-project')}>
                + New Project
            </Button>

            <Divider className="my-[10px]"/>
        </>)
};

export default UserProfilePanel;
