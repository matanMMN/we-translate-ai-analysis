'use server'

import { promises as fs } from 'fs';
import path from 'path';

export async function deleteProject(projectId: string) {
    try {
        // Get the path to userData.json
        const filePath = path.join(process.cwd(), 'src', 'data', 'userData.json');
        
        // Read the current data
        const fileContent = await fs.readFile(filePath, 'utf8');
        const projects = JSON.parse(fileContent);
        
        // Find the project index
        const projectIndex = projects.findIndex((project: any) => project.id === projectId);
        
        if (projectIndex === -1) {
            throw new Error('Project not found');
        }
        
        // Remove the project
        projects.splice(projectIndex, 1);
        
        // Write the updated data back to the file
        await fs.writeFile(filePath, JSON.stringify(projects, null, 2), 'utf8');
        
        return true;
    } catch (error) {
        console.error('Error deleting project:', error);
        return false;
    }
} 