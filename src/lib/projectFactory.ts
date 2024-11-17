import {getUser} from "@/lib/AuthGuard";

interface NewProjectData {
    title: string;
    description: string;
    sourceLanguage: string;
    destinationLanguage: string;
    industry: string;
    referenceFile: File;
    accessToken: string | undefined;
}


export const createNewProject = async (data: NewProjectData) => {

    if (!data.accessToken) {
        throw new Error('User not authenticated');
    }

    // upload the reference file first
    const formData = new FormData();
    formData.append('file', data.referenceFile);
    const uploadRes = await fetch(`http://localhost:8000/files/upload/`, {
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


    const res = await fetch('http://localhost:8000/jobs', {
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
            // reference_file: data.referenceFile,
            // members: members,
            // currentUser: data.currentUser
        })
    })

    const project = await res.json();

    if (project.status_code >= 400)
        throw {
            error: Error("Failed to create project"),
            reason: 'Project name is already taken'
        }

    if (project.status_code === 201) {
        const injectFileIdRes = await fetch(`http://localhost:8000/jobs/${project.data.id}`, {
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
            dueDate: project.data.dueDate ? new Date(projectData.data.dueDate).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
            createdAt: project.data.createdAt ? new Date(projectData.data.createdAt).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
            updatedAt: project.data.updatedAt ? new Date(projectData.data.updatedAt).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
            // activities: project.data.activities.map((activity: any) => ({
            //     ...activity,
            //     timestamp: new Date(activity.timestamp).toLocaleDateString("en")
            // }))
        }
    }

    // return {
    //     id: crypto.randomUUID(),
    //     clientId: crypto.randomUUID(),
    //     sourceFileId: crypto.randomUUID(),
    //     destFileId: crypto.randomUUID(),
    //     reference_file_id: crypto.randomUUID(),
    //
    //     name: data.name,
    //     description: data.description,
    //     sourceLanguage: data.sourceLanguage,
    //     destinationLanguage: data.destinationLanguage,
    //
    //     priority: 'Normal',
    //     status: 'Planned',
    //     currentStepIndex: 0,
    //
    //     comments: ["Initial setup"],
    //     members: members,
    //     activities: [
    //         {
    //             id: crypto.randomUUID(),
    //             user: members[0],
    //             action: 'created the project',
    //             timestamp: now.toLocaleDateString()
    //         }
    //     ],
    //
    //     dueDate: new Date(now.setMonth(now.getMonth() + 1)).toLocaleDateString("en"),
    //     createdAt: now.toLocaleDateString("en"),
    //     updatedAt: now.toLocaleDateString("en"),
    //
    //     currentUser,
    //     createdBy: currentUser,
    //     updatedBy: currentUser,
    //
    //     deletedAt: undefined,
    //     deletedBy: undefined,
    //     approvedAt: undefined,
    //     approvedBy: undefined
    // };
};


export const checkProjectName = async (name: string) => {
    const user = await getUser()
    const accessToken = user?.accessToken;
    const res = await fetch(`http://localhost:8000/jobs`, {
        headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        }
    });
    const projects = await res.json();
    return projects.data.some((project: any) => project.title === name);
}