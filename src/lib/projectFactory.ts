import { Project, User } from '@/lib/userData';
import { members } from '@/lib/userData';

interface NewProjectData {
    name: string;
    description: string;
    sourceLanguage: string;
    destinationLanguage: string;
    industry: string;
    referenceFile: string;
    currentUser: User;
}

export const createNewProject = async (data: NewProjectData): Promise<Project> => {
    const now = new Date();
    const { currentUser } = data;
    
    return {
        id: crypto.randomUUID(),
        clientId: crypto.randomUUID(),
        sourceFileId: crypto.randomUUID(),
        destFileId: crypto.randomUUID(),
        reference_file_id: crypto.randomUUID(),
        
        name: data.name,
        description: data.description,
        sourceLanguage: data.sourceLanguage,
        destinationLanguage: data.destinationLanguage,
        
        priority: 'Normal',
        status: 'Planned',
        currentStepIndex: 0,
        
        comments: ["Initial setup"],
        members: members,
        activities: [
            {
                id: crypto.randomUUID(),
                user: members[0],
                action: 'created the project',
                timestamp: now.toLocaleDateString()
            }
        ],
        
        dueDate: new Date(now.setMonth(now.getMonth() + 1)).toLocaleDateString("en"),
        createdAt: now.toLocaleDateString("en"),
        updatedAt: now.toLocaleDateString("en"),
        
        currentUser,
        createdBy: currentUser,
        updatedBy: currentUser,
        
        deletedAt: undefined,
        deletedBy: undefined,
        approvedAt: undefined,
        approvedBy: undefined
    };
}; 