"use server"

import {Project} from "@/lib/userData";
import {getUser} from "@/lib/AuthGuard";
import fs from 'fs/promises';
import path from 'path';
import {revalidatePath} from "next/cache";


export const fetchProjects = async (): Promise<Project[]> => {
    try {
        const projects = await import('@/data/userData.json');
        return projects.default.map((project: Project) => ({
            ...project,
            dueDate: project.dueDate ? new Date(project.dueDate).toLocaleDateString("en") : undefined,
            createdAt: project.createdAt ? new Date(project.createdAt).toLocaleDateString("en") : undefined,
            updatedAt: project.updatedAt ? new Date(project.updatedAt).toLocaleDateString("en") : undefined,

        }))
    } catch (error) {
        console.error('Error fetching projects:', error);
        return []
    }
}

export async function getUserProjects() {
    const user = await getUser();
    return user?.userData?.allProjects

}


export async function getUserProject(projectId: string) {
    const user = await getUser();
    return user?.userData?.allProjects?.find((p: Project) => p.id == projectId)
}

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
        // Get the path to the JSON file
        const filePath = path.join(process.cwd(), 'src', 'data', 'userData.json');

        // Read projects file
        const fileContent = await fs.readFile(filePath, 'utf-8');
        const projects: Project[] = JSON.parse(fileContent);

        // Find the specific project
        const project = projects.find(p => p.id.toString() === projectId.toString());

        if (!project) {
            console.log(`Project with ID ${projectId} not found`);
            return null;
        }

        // Format dates if they exist
        return {
            ...project,
            createdAt: project.createdAt ? new Date(project.createdAt).toLocaleDateString("en") : undefined,
            updatedAt: project.updatedAt ? new Date(project.updatedAt).toLocaleDateString("en") : undefined,
            dueDate: project.dueDate ? new Date(project.dueDate).toLocaleDateString("en") : undefined,
        };

    } catch (error) {
        console.error('Error fetching project:', error);
        return null;
    }
}