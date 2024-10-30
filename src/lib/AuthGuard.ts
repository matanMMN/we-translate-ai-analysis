import {getServerSession} from "next-auth";
import {authOptions} from "@/app/options";

export async function AuthGuard() {
    const session = await getServerSession(authOptions);
    console.log(session)
    return !!session
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