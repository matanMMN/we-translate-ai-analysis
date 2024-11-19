'use server'

import {revalidatePath} from 'next/cache';
import {getUser} from "@/lib/AuthGuard";
import {Session} from "next-auth";
import {serverUrl} from "@/lib/functions";

export async function updateUserProfile(data: {
    first_name: string;
    last_name: string;
}) {
    try {
        const user: Session | null = await getUser();
        if (!user) {
            throw new Error('Unauthorized');
        }

        const res = await fetch(`${serverUrl}/users/${user.userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json',
                'Authorization': `Bearer ${user.accessToken}`,
            },
            body: JSON.stringify(data),
        })
        const updatedUser = await res.json();
        revalidatePath('/', "layout");
        return {success: true, user: updatedUser};
    } catch (error) {
        console.error('Error updating user:', error);
        return {success: false, error: 'Failed to update profile'};
    }
} 