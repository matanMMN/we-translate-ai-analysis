"use client"

import React, {ReactNode, useState} from 'react';
import LoadingSpinner from '@/components/LoadingSpinner';
import {useSession} from "next-auth/react";
import {Divider} from "@mui/material";
import {log} from "@/lib/log";
import {useRouter} from "next/navigation";
import EditProfileForm from './EditProfileForm';

const UserProfilePanel = (): ReactNode => {

    const {data: session, status} = useSession()
    const router = useRouter()
    const [isEditing, setIsEditing] = useState(false)
    log(`Rendering User Profile Panel with User Data of: ${session?.user.name}, loading status: ${status}`);

    return status === "loading" ? <LoadingSpinner/> : (
        <>
            <div className="flex flex-col items-center p-4 bg-[#1D3B34] mx-2 mb-2 border rounded-3xl">
                {!isEditing ? (
                    <>
                        <div className="flex flex-wrap items-center text-center mb-4">
                            <div className="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center mr-3">
                                <span className="text-[#1a3937] font-semibold">
                                    {session?.user.name!.split(' ').map(n => n[0].toUpperCase()).join('')}
                                </span>
                            </div>
                            <span className="font-normal text-xl text-white font-urbanist">
                                {session?.user.name}
                            </span>
                        </div>
                        <div className="flex gap-3 w-full justify-center">
                            <button
                                className="px-6 py-2 bg-[#1D3B34] hover:bg-[#244239] text-white border rounded-full transition-colors font-urbanist flex items-center"
                                onClick={() => setIsEditing(true)}
                            >
                                <span className="text-base">Edit Profile</span>
                            </button>
                            <button
                                className="px-6 py-2 bg-[#1D3B34] hover:bg-[#244239] text-white border rounded-full transition-colors font-urbanist flex items-center"
                                onClick={() => router.push('/new-project')}
                            >
                                <span className="mr-1 text-xl">+</span>
                                <span className="text-base">New Project</span>
                            </button>
                        </div>
                    </>
                ) : (
                    <EditProfileForm onCancel={() => setIsEditing(false)} />
                )}
            </div>
            <Divider className="my-[10px]"/>
        </>
    )
};

export default UserProfilePanel;
