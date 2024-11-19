'use server'


import {serverUrl} from "@/lib/functions";

export async function deleteProject(projectId: string, accessToken: string): Promise<boolean> {
    try {

        const res = await fetch(`${serverUrl}/jobs/${projectId}`, {
            method: 'DELETE',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (res.status === 200)
            return true;
        else throw new Error("Failed to delete project")

    } catch (error) {
        console.error('Error deleting project:', error);
        return false;
    }
} 