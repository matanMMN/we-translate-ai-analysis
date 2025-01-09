"use server"

import { getUser } from "@/lib/AuthGuard"
import { serverUrl } from "@/lib/functions"

export async function getAllUsers() {
    const session = await getUser()
    const response = await fetch(`${serverUrl}/users`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session?.accessToken}`,
        },
    })
    const data = await response.json()
    return data.data
}


export async function updateUserRole(data :{userId: string, newRole: string}) {
    const session = await getUser()
    const response = await fetch(`${serverUrl}/users/${data.userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session?.accessToken}`,
        },
        body: JSON.stringify({
            role: data.newRole
        })
    })
    const update = await response.json()
    return update.data
}
