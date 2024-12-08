'use client'

import {useState} from "react";
import {useSelector} from "react-redux";
import {selectSession, setSessionSlice} from "@/store/slices/sessionSlice";
import {toast} from "sonner"
import ProjectInfo from "./sections/ProjectInfo";
import ProjectDescription from "./sections/ProjectDescription";
import ProjectMembers from "./sections/ProjectMembers";
import ProjectActivity from "./sections/ProjectActivity";
import {staticActivities, staticMembers} from "@/data/staticData";
import {UnsavedChangesDialog} from "@/components/project-details/UnsavedChangesDialog"
import {Project} from "@/lib/userData";
import {useAppDispatch} from "@/hooks/useAppDispatch";
import EditOrViewGrid from "@/components/editor/EditOrViewGrid"
import {updateProjectData} from "@/actions/updateProject";
// const EditOrViewGrid = dynamic(
//     () => import("@/components/editor/EditOrViewGrid"),
//     {
//         loading: () => <div className="h-20 animate-pulse bg-gray-200 rounded-md"/>,
//         ssr: false
//     }
// );

export default function ProjectDetails() {

    const {project, userSession} = useSelector(selectSession);
    const session = useSelector(selectSession);
    const dispatch = useAppDispatch()
    const [isEditing, setIsEditing] = useState(false);

    const [editedProject, setEditedProject] = useState({
        priority: project?.priority,
        status: project?.status,
        description: project?.description,
        due_date: project?.due_date
    });
    const [showUnsavedDialog, setShowUnsavedDialog] = useState(false);
    // const dispatch = useDispatch();
    if (!project) return null;

    const handleCancel = () => {
        setEditedProject({
            priority: project?.priority,
            status: project?.status,
            description: project?.description,
            due_date: project?.due_date
        })
        setIsEditing(false);
    };

    const handleSave = async () => {
        if (editedProject.due_date !== new Date(editedProject.due_date!).toISOString())
            editedProject.due_date = new Date(editedProject.due_date!).toISOString();

        const updatedProject = await updateProjectData({
            projectId: project.id,
            editedProject
        });
        setIsEditing(false);

        toast("Project updated successfully");
        console.log(updatedProject, editedProject)
        dispatch(setSessionSlice({
            ...session, project: {
                ...updatedProject.data,
                due_date: updatedProject.data.due_date ? new Date(updatedProject.data.due_date).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
                created_at: updatedProject.data.created_at ? new Date(updatedProject.data.created_at).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
                updated_at: updatedProject.data.updated_at ? new Date(updatedProject.data.updated_at).toLocaleDateString("en") : new Date(Date.now()).toLocaleDateString("en"),
            }
        }));
    };

    const handleCancelClick = () => {
        if (JSON.stringify({
            priority: project?.priority,
            status: project?.status,
            description: project?.description,
            due_date: project?.due_date
        }) !== JSON.stringify(editedProject)) {
            setShowUnsavedDialog(true);
        } else {
            handleCancel();
        }
    };

    const handleConfirmDiscard = () => {
        setShowUnsavedDialog(false);
        handleCancel();
    };

    const handleDescriptionChange = (description: string) => {
        setEditedProject((prev: any) => {
            return {
                ...prev,
                description
            }
        });
    };

    const handleProjectFieldsChange = (updatedFields: Partial<typeof project>) => {
        console.log(updatedFields)
        setEditedProject((prev: any) => {
            return {
                ...prev,
                ...updatedFields
            }
        });
    };

    return (
        <div className="space-y-8">
            <ProjectInfo
                project={project as Project}
                editProject={editedProject as Project}
                isEditing={isEditing}
                onEditAction={() => setIsEditing(true)}
                onSaveAction={handleSave}
                onCancelAction={handleCancelClick}
                onChangeAction={handleProjectFieldsChange}
            />
            <ProjectDescription
                description={isEditing ? editedProject?.description as string : project?.description as string}
                isEditing={isEditing}
                onDescriptionChangeAction={handleDescriptionChange}
            />
            {userSession && <EditOrViewGrid/>}
            <div className="grid grid-cols-2 gap-8">
                <ProjectMembers members={project.members || staticMembers}/>
                <ProjectActivity activities={project.activities || staticActivities}/>
            </div>
            <UnsavedChangesDialog
                isOpen={showUnsavedDialog}
                onConfirm={handleConfirmDiscard}
                onCancel={() => setShowUnsavedDialog(false)}
            />
        </div>
    );
}