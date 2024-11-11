"use client"

import {useEffect, useState} from 'react'
import {useRouter} from 'next/navigation'
import {useDispatch, useSelector} from 'react-redux'
import {useForm, UseFormReturn} from "react-hook-form"
import {zodResolver} from "@hookform/resolvers/zod"
import * as z from "zod"
import {toast} from 'sonner'
import React from 'react'

import {setSessionSlice, selectSession} from '@/store/slices/sessionSlice'
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card"
import {Button} from "@/components/ui/button"
import {CustomProjectFormField} from './ProjectFormField'
import {ProjectForm} from './ProjectForm'
import UploadFileModal from './UploadFileModal'
import {Project, User} from "@/lib/userData";
import {AlertCircle} from "lucide-react"
import {cn} from "@/lib/utils"
import {getUser} from "@/lib/AuthGuard";
import {saveNewProject} from '@/actions/getUserProjects';

// Enhanced form schema with stricter validation
const formSchema = z.object({
    name: z.string()
        .min(3, {message: "Name must be at least 3 characters"})
        .max(50, {message: "Name must be less than 50 characters"})
        .regex(/^[a-zA-Z0-9\s-]+$/, {
            message: "Name can only contain letters, numbers, spaces, and hyphens"
        }),
    description: z.string()
        .min(10, {message: "Description must be at least 10 characters"})
        .max(500, {message: "Description must be less than 500 characters"}),
    industry: z.enum(["Cosmetics", "Leaflets", "Medical Devices"], {
        required_error: "Please select an industry",
    }),
    sourceLanguage: z.enum(["en", "he"], {
        required_error: "Please select a source language",
    }),
    destinationLanguage: z.enum(["en", "he", "ar"], {
        required_error: "Please select a target language",
    }),
    referenceFile: z.string().min(1, {message: "Reference file is required"}),
}).refine(
    (data) => data.sourceLanguage !== data.destinationLanguage,
    {
        message: "Target language must be different from source language",
        path: ["destinationLanguage"], // This will show the error on the destinationLanguage field
    }
);

type FormData = z.infer<typeof formSchema>

const industryOptions = [
    {value: "Cosmetics", label: "Cosmetics"},
    {value: "Leaflets", label: "Leaflets"},
    {value: "Medical Devices", label: "Medical Devices"}
]

const sourceLanguageOptions = [
    {value: "en", label: "English"},
    {value: "he", label: "Hebrew"}
]

const targetLanguageOptions = [
    {value: "en", label: "English"},
    {value: "he", label: "Hebrew"},
    {value: "ar", label: "Arabic"}
]

export default function NewProjectForm() {
    const router = useRouter()
    const dispatch = useDispatch()
    const sessionState = useSelector(selectSession)
    const {userData} = sessionState.userSession || {}
    const [isSubmitting, setIsSubmitting] = useState(false)
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [showUploadModal, setShowUploadModal] = useState(false)
    console.log(sessionState)
    useEffect(() => {
        const prepareSession = async () => {
            dispatch(setSessionSlice({
                projectId: "",
                userSession: await getUser(),
                project: "" as unknown as Project
            }))
        }
        prepareSession()
    }, [dispatch])


    const form = useForm<FormData>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: '',
            description: '',
            industry: undefined,
            sourceLanguage: undefined,
            destinationLanguage: undefined,
            referenceFile: ''
        },
        mode: 'onTouched', // Enable real-time validation
    })

    // Watch for language changes to validate the combination
    const sourceLanguage = form.watch('sourceLanguage')
    const destinationLanguage = form.watch('destinationLanguage')

    useEffect(() => {
        if (sourceLanguage && destinationLanguage) {
            form.trigger('destinationLanguage')
        }
    }, [sourceLanguage, destinationLanguage, form])

    const handleUpload = (files: File[]) => {
        if (files.length > 0) {
            setSelectedFile(files[0])
            form.setValue('referenceFile', files[0].name)
            setShowUploadModal(false)
        }
    }

    const handleSubmit = async (data: FormData) => {
        // Check if form has any errors
        const isValid = await form.trigger();
        if (!isValid) {
            // Show toast with all validation errors
            toast.error(
                <div className="space-y-2">
                    <div className="font-semibold">Please fix the following errors:</div>
                    <ul className="list-disc pl-4">
                        {Object.entries(form.formState.errors).map(([field, error]) => (
                            <li key={field} className="capitalize">
                                {field.replace(/([A-Z])/g, ' $1').toLowerCase()}: {error.message}
                            </li>
                        ))}
                    </ul>
                </div>
            );
            return;
        }
        if (!selectedFile) {
            toast.error('Please select a reference file');
            return;
        }

        setIsSubmitting(true);

        try {
            // Create new project object

            const user = {
                id: userData!.id,
                name: userData?.first_name + ' ' + userData?.last_name,
                avatar: "/assets/user1avatar.svg"
            }

            const newProject: Project = {
                id: crypto.randomUUID(),
                clientId: crypto.randomUUID(),
                //      "sourceFileId": 1,
                //     "destFileId": 2,
                //     "reference_file_id": 10,
                name: data.name,
                description: data.description,
                sourceLanguage: data.sourceLanguage,
                destinationLanguage: data.destinationLanguage,
                status: 'Planned',
                priority: 'Normal',
                currentStepIndex: 1,
                comments: ['Initial project setup'],
                members: [
                    user
                ],
                activities: [
                    {
                        id: userData!.id,
                        user,
                        action: "started the project",
                        timestamp: new Date().toISOString()
                    }
                ],
                dueDate: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
                createdBy: user as unknown as User,
                currentUser: user as unknown as User,
                updatedAt: new Date().toISOString(),
                updatedBy: user as unknown as User,
                createdAt: new Date().toISOString(),
                // Add other required Project fields here
            };

            // Save to JSON file
            const saved = await saveNewProject(newProject);

            if (!saved) {
                throw new Error('Failed to save project');
            }

            // Update Redux state
            // const currentProjects = sessionState.userSession?.userData?.allProjects || [];
            // dispatch(setSessionSlice({
            //     ...sessionState,
            //     userSession: {
            //         ...sessionState.userSession!,
            //         userData: {
            //             ...sessionState.userSession!.userData as User,
            //             allProjects: [newProject, ...currentProjects]
            //         }
            //     }
            // }));

            if (saved) {
                toast.success('Project created successfully');

                // Close the modal first by navigating back
                router.back();

                // Then navigate to the new project after a brief delay
                setTimeout(() => {
                    router.push(`/${newProject.id}/details`);
                }, 100);
            }

        } catch (error) {
            console.error('Failed to create project:', error);
            toast.error('Failed to create project');
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <Card className="w-full max-w-md">
            <CardHeader>
                <CardTitle className="text-center">Project Details</CardTitle>
            </CardHeader>
            <CardContent>
                <ProjectForm {...form}>
                    <form
                        onSubmit={form.handleSubmit(handleSubmit)}
                        className="space-y-4"
                    >
                        <CustomProjectFormField
                            form={form as unknown as UseFormReturn}
                            name="name"
                            label="Project Name"
                            placeholder="Enter project name"
                            type="input"
                            required
                        />

                        <CustomProjectFormField
                            form={form as unknown as UseFormReturn}
                            name="description"
                            label="Description"
                            placeholder="Enter project description"
                            type="textarea"
                            required
                        />

                        <CustomProjectFormField
                            form={form as unknown as UseFormReturn}
                            name="industry"
                            label="Industry"
                            placeholder="Select industry"
                            type="select"
                            options={industryOptions}
                            required
                        />

                        <div className="grid grid-cols-2 gap-4">
                            <CustomProjectFormField
                                form={form as unknown as UseFormReturn}
                                name="sourceLanguage"
                                label="Source Language"
                                placeholder="Select source"
                                type="select"
                                options={sourceLanguageOptions}
                                required
                            />

                            <CustomProjectFormField
                                form={form as unknown as UseFormReturn}
                                name="destinationLanguage"
                                label="Target Language"
                                placeholder="Select target"
                                type="select"
                                options={targetLanguageOptions}
                                required
                            />
                        </div>

                        <div className="space-y-2">
                            <div className="flex items-center gap-1">
                                <span className="text-sm font-medium">Reference File</span>
                                <span className="text-red-500">*</span>
                                {form.formState.errors.referenceFile && (
                                    <AlertCircle className="w-4 h-4 text-red-500"/>
                                )}
                            </div>
                            <Button
                                type="button"
                                variant="outline"
                                className={cn(
                                    "w-full",
                                    form.formState.errors.referenceFile &&
                                    "border-red-500 focus-visible:ring-red-500"
                                )}
                                onClick={() => setShowUploadModal(true)}
                            >
                                {selectedFile ? selectedFile.name : "Add reference file"}
                            </Button>
                            {form.formState.errors.referenceFile && (
                                <p className="text-sm font-medium text-red-500">
                                    {form.formState.errors.referenceFile.message}
                                </p>
                            )}
                        </div>

                        <Button
                            type="submit"
                            className="w-full bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'Creating Project...' : 'Start a Project'}
                        </Button>
                    </form>
                </ProjectForm>
            </CardContent>

            {showUploadModal && (
                <UploadFileModal
                    open={showUploadModal}
                    onClose={() => setShowUploadModal(false)}
                    onUpload={handleUpload}
                />
            )}
        </Card>
    )
}

