"use server"


import {Project} from "@/lib/userData";

export default async function getUserProjects() {
    const allProjects: Array<Project> = await new Promise(() => setTimeout(() => {
        return allProjects
    }, 3000))

    return allProjects
}