"use server"

import {getServerSession} from "next-auth";
import {authOptions} from "@/app/options";
import {cache} from "react";
import {redirect} from "next/navigation";

export const AuthGuard = cache(async () => {
    const session = await getServerSession(authOptions);
    if (!session)
        redirect('/login')

    return !!session
})

export const protectLogin = cache(async () => {
    const session = await getServerSession(authOptions);
    if (session)
        redirect('/')

    return !!session

})

export const verifySession = async () => {
    const session = await getServerSession(authOptions);

    if (!session?.user) {
        redirect('/login')
    }

    return {isAuth: true, userSession: session}
}


export const getUser = async () => {


    const session = await verifySession()
    if (!session) {
        return null
    }

    try {
        // const response = await fetch('/api/user', {
        //     method: 'GET',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     }
        // })
        return session.userSession
    } catch (error) {
        console.log("Failed to fetch user", error)
        return null
    }
}

// export async function AuthGuardAdmin() {
//     const session = await getServerSession(authOptions);
//     return (session && session.user.role === 'ADMIN');
//
// }
//
// export async function getUserId() {
//     const session = await getServerSession(authOptions);
//     return session?.user.userId;
// }