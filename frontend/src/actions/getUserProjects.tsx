"use server"


import {Project} from "@/lib/userData";
import {getUser} from "@/lib/AuthGuard";
import fs from 'fs/promises';
import path from 'path';
import {revalidatePath} from "next/cache";
import {serverUrl} from "@/lib/functions";


export const fetchProjects = async (): Promise<Project[]> => {
    try {
        const user = await getUser();
        const res = await fetch(`${serverUrl}/jobs`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${user?.accessToken}`
            },
        })

        const projects = await res.json();
        if (projects && projects.status_code === 200)
            return projects.data;
        else
            throw new Error("Failed to fetch user projects")
    } catch (error) {
        console.error('Error fetching projects:', error);
        return []
    }
}
//
// export async function getUserProjects() {
//     const user = await getUser();
//     return user?.userData?.allProjects
//
// }

//
// export async function getUserProject(projectId: string) {
//     const user = await getUser();
//     return user?.userData?.allProjects?.find((p: Project) => p.id == projectId)
// }

export const saveNewProject = async (project: Project): Promise<boolean> => {
    try {
        // Get the path to the JSON file
        const filePath = path.join(process.cwd(), 'src', 'data', 'userData.json');

        // Read existing projects
        const fileContent = await fs.readFile(filePath, 'utf-8');
        const projects: Project[] = JSON.parse(fileContent);

        // Add new project to the beginning of the array
        projects.unshift(project);

        // Write back to file
        await fs.writeFile(filePath, JSON.stringify(projects, null, 2), 'utf-8');
        revalidatePath('/')
        return true;
    } catch (error) {
        console.error('Error saving project:', error);
        return false;
    }
}

export const fetchProjectById = async (projectId: string): Promise<Project | null> => {
    try {
        const user = await getUser();
        const res = await fetch(`${serverUrl}/jobs/${projectId}`, {
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${user?.accessToken}`
            }
        })
        const project = await res.json();
        if (project.status_code === 200) {
            // Project fetch succeed, feed caches before returning.
            /* TODO */
            return {
                ...project.data,
                due_date: project.data.due_date ? new Date(project.data.due_date).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
                created_at: project.data.created_at ? new Date(project.data.created_at).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
                updated_at: project.data.updated_at ? new Date(project.data.updated_at).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
            }
        } else
            throw new Error("Failed to fetch project")
        // // Get the path to the JSON file
        // const filePath = path.join(process.cwd(), 'src', 'data', 'userData.json');
        //
        // // Read projects file
        // const fileContent = await fs.readFile(filePath, 'utf-8');
        // const projects: Project[] = JSON.parse(fileContent);
        //
        // // Find the specific project
        // const project = projects.find(p => p.id.toString() === projectId.toString());
        //
        // if (!project) {
        //     console.log(`Project with ID ${projectId} not found`);
        //     return null;
        // }
        //
        // // Format dates if they exist
        // return {
        //     ...project,
        //     createdAt: project.createdAt ? new Date(project.createdAt).toLocaleDateString("en") : undefined,
        //     updatedAt: project.updatedAt ? new Date(project.updatedAt).toLocaleDateString("en") : undefined,
        //     dueDate: project.dueDate ? new Date(project.dueDate).toLocaleDateString("en") : undefined,
        // };

    } catch (error) {
        console.error('Error fetching project:', error);
        return null;
    }
}