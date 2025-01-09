import avatar1 from '@/assets/user1avatar.svg'
import avatar2 from '@/assets/user2avatar.svg'
import { UserRole } from '@/types/roles';

//
// const getPriority = () => {
//     return ['Low', 'Normal', 'High', 'Critical'][Math.floor(Math.random() * 4)];
// }

export const getStatus = () => {
    return ['Planned', 'In Progress', 'Completed', 'On Hold'][Math.floor(Math.random() * 4)] as Project['status']
}


// export const srcFile = new Blob([fs.readFileSync(path.join(process.cwd(), 'src', 'assets', 'src.txt'), 'utf-8')], {type: 'text/plain'})


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
    allProjects?: Array<Project>
    role: UserRole
}

export interface ProjectMember {
    id: string
    name: string
    avatar?: string
}

export interface ActivityItem {
    id: string
    user: ProjectMember
    action: string
    timestamp: string
}

export const members: ProjectMember[] = [
    {id: '1', name: 'Aviram Shabtay', avatar: avatar1.src},
    {id: '2', name: 'Emma K.', avatar: avatar2.src},
]

export const user = {
    id: "1",
    role_id: 1,
    first_name: "Aviram",
    last_name: "Shabtay",
    username: "admin",
    password: "admin",
    email: "admin@admin.ad",
    created_at: "28.10.2024",
    updated_at: "28.10.2024",
    created_by: "admin",
    updated_by: "admin",
    settings: null,
    auth: true,
    accessToken: "access",
    allProjects: [
        {
            id: 1,
            clientId: 1,
            sourceFileId: 1,
            destFileId: 2,
            reference_file_id: 10,
            name: "Fostimon",
            description: "The translation of the Fostimon medicine for injection.",
            sourceLanguage: "Hebrew",
            destinationLanguage: "English",
            // priority: getPriority(),
            priority: 'High',
            status: getStatus(),
            currentStepIndex: 2,
            comments: ["Initial setup", "Translation started"],
            members: members,
            activities: [
                {
                    id: '1',
                    user: members[0],
                    action: 'deleted the word "slovent"',
                    timestamp: '2 days ago'
                },
                {
                    id: '2',
                    user: members[1],
                    action: 'changed the name of the project',
                    timestamp: '3 days ago'
                },
                {
                    id: '3',
                    user: members[0],
                    action: 'started the project',
                    timestamp: '4 days ago'
                },
            ],
            dueDate: new Date("2024-12-31").toLocaleDateString("en"),
            currentUser: "Miri hazan",
            createdAt: new Date("2024-10-28").toLocaleDateString("en"),
            createdBy: "Miri hazan",
            updatedAt: new Date("2024-10-29").toLocaleDateString("en"),
            updatedBy: "Miri hazan",
            deletedAt: undefined,
            deletedBy: undefined,
            approvedAt: undefined,
            approvedBy: undefined
        },
        {
            id: 2,
            clientId: 2,
            sourceFileId: 3,
            destFileId: 4,
            reference_file_id: 10,
            name: "Fluoxetine",
            description: "The translation of the Fostimon medicine for injection.",
            sourceLanguage: "English",
            destinationLanguage: "Hebrew",
            // priority: getPriority(),
            // priority: getPriority(),
            priority: 'Critical',
            status: getStatus(),
            currentStepIndex: 1,
            comments: ["Initial setup", "Translation started"],
            members: members,
            activities: [
                {
                    id: '1',
                    user: members[0],
                    action: 'deleted the word "slovent"',
                    timestamp: '2 days ago'
                },
                {
                    id: '2',
                    user: members[1],
                    action: 'changed the name of the project',
                    timestamp: '3 days ago'
                },
                {
                    id: '3',
                    user: members[0],
                    action: 'started the project',
                    timestamp: '4 days ago'
                },
            ],
            dueDate: new Date("2024-11-30").toLocaleDateString("en"),
            currentUser: "Miri hazan",
            createdAt: new Date("2024-10-28").toLocaleDateString("en"),
            createdBy: "Miri hazan",
            updatedAt: new Date("2024-10-29").toLocaleDateString("en"),
            updatedBy: "Miri hazan",
            deletedAt: undefined,
            deletedBy: undefined,
            approvedAt: undefined,
            approvedBy: undefined
        },
        {
            id: 3,
            clientId: 3,
            sourceFileId: 5,
            destFileId: 6,
            reference_file_id: 10,
            name: "Finasteride",
            description: "The translation of the Fostimon medicine for injection.",
            sourceLanguage: "English",
            destinationLanguage: "Hebrew",
            // priority: getPriority(),
            priority: 'Low',
            status: getStatus(),
            currentStepIndex: 3,
            comments: ["Initial setup", "Translation started", "Review in progress"],
            members: members,
            activities: [
                {
                    id: '1',
                    user: members[0],
                    action: 'deleted the word "slovent"',
                    timestamp: '2 days ago'
                },
                {
                    id: '2',
                    user: members[1],
                    action: 'changed the name of the project',
                    timestamp: '3 days ago'
                },
                {
                    id: '3',
                    user: members[0],
                    action: 'started the project',
                    timestamp: '4 days ago'
                },
            ],
            dueDate: new Date("2024-10-31").toLocaleDateString("en"),
            currentUser: "Miri hazan",
            createdAt: new Date("2024-10-28").toLocaleDateString("en"),
            createdBy: "Miri hazan",
            updatedAt: new Date("2024-10-29").toLocaleDateString("en"),
            updatedBy: "Miri hazan",
            deletedAt: undefined,
            deletedBy: undefined,
            approvedAt: undefined,
            approvedBy: undefined
        },
        {
            id: 4,
            clientId: 4,
            sourceFileId: 7,
            destFileId: 8,
            reference_file_id: 10,
            name: "Fluconazole",
            description: "The translation of the Fostimon medicine for injection.",
            sourceLanguage: "English",
            destinationLanguage: "Hebrew",
            // priority: getPriority(),
            priority: 'Normal',
            status: getStatus(),
            currentStepIndex: 0,
            comments: ["Initial setup", "Translation started"],
            members: members,
            activities: [
                {
                    id: '1',
                    user: members[0],
                    action: 'deleted the word "slovent"',
                    timestamp: '2 days ago'
                },
                {
                    id: '2',
                    user: members[1],
                    action: 'changed the name of the project',
                    timestamp: '3 days ago'
                },
                {
                    id: '3',
                    user: members[0],
                    action: 'started the project',
                    timestamp: '4 days ago'
                },
            ],
            dueDate: new Date("2024-12-15").toLocaleDateString("en"),
            currentUser: "Miri hazan",
            createdAt: new Date("2024-10-28").toLocaleDateString("en"),
            createdBy: "Miri hazan",
            updatedAt: new Date("2024-10-29").toLocaleDateString("en"),
            updatedBy: "Miri hazan",
            deletedAt: undefined,
            deletedBy: undefined,
            approvedAt: undefined,
            approvedBy: undefined
        }
    ]

}

export interface Project {
    id: number | string;
    client_id?: number | string;
    source_file_id?: number | string;
    destFileId?: number | string;
    description: string,
    reference_file_id?: number | string;
    target_file_id?: number | string;
    title: string;
    source_language: string;
    is_translating: boolean;
    target_language: string;
    priority: number | string;
    status?: string;
    data: any;
    current_step_index?: number;
    // data: any;
    // settings: any;
    comments?: Array<string>
    activities?: Array<ActivityItem>
    members?: Array<ProjectMember>
    due_date?: string;
    current_user?: User;
    created_at: string;
    created_by?: User
    updated_at?: string;
    updated_by?: User;
    deleted_at?: string | undefined
    deleted_by?: User | undefined
    approved_at?: string | undefined
    approved_by?: User | undefined
}
