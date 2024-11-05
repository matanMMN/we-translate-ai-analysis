"use server"


import {Project} from "@/lib/userData";
import {getUser} from "@/lib/AuthGuard";

export async function getUserProjects() {
    const user = await getUser();
    return user?.userData?.allProjects

}


export async function getUserProject(projectId: string) {
    const user = await getUser();
    return user?.userData?.allProjects?.find((p: Project) => p.id == projectId)
}