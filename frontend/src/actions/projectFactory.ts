"use server"

import {getUser} from "@/lib/AuthGuard";
import {serverUrl} from "@/lib/functions";

interface NewProjectData {
    title: string;
    description: string;
    sourceLanguage: string;
    destinationLanguage: string;
    // industry: string;
    referenceFile: File;
    accessToken: string | undefined;
}


export const createNewProject = async (data: NewProjectData) => {

    if (!data.accessToken) {
        throw new Error('User not authenticated');
    }

    const formData = new FormData();
    formData.append('file', data.referenceFile);
    const uploadRes = await fetch(`${serverUrl}/files/upload/`, {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${data.accessToken}`
        },
        body: formData
    });

    const fileId = await uploadRes.json();


    if (uploadRes.status >= 400)
        throw new Error("Failed to upload reference file")


    const res = await fetch(`${serverUrl}/jobs`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'Authorization': `Bearer ${data.accessToken}`
        },
        body: JSON.stringify({
            title: data.title,
            description: data.description,
            source_language: data.sourceLanguage,
            target_language: data.destinationLanguage,
            due_date: new Date(Date.now()).toISOString()
        })
    })

    const project = await res.json();

    if (project.status_code >= 400)
        throw {
            error: Error("Failed to create project"),
            reason: 'Project name is already taken'
        }

    if (project.status_code === 201) {
        const injectFileIdRes = await fetch(`${serverUrl}/jobs/${project.data.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json',
                'Authorization': `Bearer ${data.accessToken}`
            },
            body: JSON.stringify({reference_file_id: fileId.data.id})
        })
        const projectData = await injectFileIdRes.json()
        console.log(projectData)
        return {
            ...projectData.data,
            due_date: project.data.dueDate ? new Date(projectData.data.dueDate).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
            created_at: project.data.createdAt ? new Date(projectData.data.createdAt).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
            updated_at: project.data.updatedAt ? new Date(projectData.data.updatedAt).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
        }
    }
};


export const checkProjectName = async (name: string) => {
    const user = await getUser()
    const accessToken = user?.accessToken;
    const res = await fetch(`${serverUrl}/jobs`, {
        headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        }
    });
    const projects = await res.json();
    return projects.data.some((project: any) => project.title === name);
}