export interface User {
    id: string;
    role_id: number;
    first_name: string;
    last_name: string;
    username: string;
    password: string;
    email: string;
    created_at: string;
    updated_at: string;
    created_by: string;
    updated_by: string;
    settings: null;
    auth: boolean;
    accessToken: string;
}

export const user = {
    id: "1",
    role_id: 1,
    first_name: "Admin",
    last_name: "Adminel",
    username: "admin",
    password: "admin",
    email: "admin@admin.ad",
    created_at: "28.10.2024",
    updated_at: "28.10.2024",
    created_by: "admin",
    updated_by: "admin",
    settings: null,
    auth: true,
    accessToken: "access"
}

export interface Project {
    id: number | string;
    clientId: number | string;
    sourceFileId: number | string;
    destFileId: number | string;
    sourceLanguage: string;
    destLanguage: string;
    priority: number;
    status: string;
    currentStepIndex: number;
    // data: any;
    // settings: any;
    comments: Array<string>
    dueDate: Date;
    currentUser: User;
    createdAt: Date;
    createdBy: User
    updatedAt: Date;
    updatedBy: User;
    deletedAt: Date | undefined
    deletedBy: User | undefined
    approvedAt: Date | undefined
    approvedBy: User | undefined
}

export const allProjects: Array<Project> = [
    {
        id: 1,
        clientId: 1,
        sourceFileId: 1,
        destFileId: 2,
        sourceLanguage: "en",
        destLanguage: "es",
        priority: 1,
        status: "in-progress",
        currentStepIndex: 2,
        // data: {},
        // settings: {},
        comments: ["Initial setup", "Translation started"],
        dueDate: new Date("2024-12-31"),
        currentUser: user,
        createdAt: new Date("2024-10-28"),
        createdBy: user,
        updatedAt: new Date("2024-10-29"),
        updatedBy: user,
        deletedAt: undefined,
        deletedBy: undefined,
        approvedAt: undefined,
        approvedBy: undefined
    }
]