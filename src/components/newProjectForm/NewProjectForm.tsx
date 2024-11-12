"use client"

import {useCallback, useMemo, useState} from 'react';
import {useForm} from 'react-hook-form';
import {zodResolver} from '@hookform/resolvers/zod';
import * as z from 'zod';
import {ProjectForm} from './ProjectForm';
import FormField from './FormField';
import {Button} from '@/components/ui/button';
import {useRouter} from 'next/navigation';
import {toast} from 'sonner';
import {saveNewProject} from '@/actions/getUserProjects';
import {createNewProject} from '@/lib/projectFactory';
import {useSession} from 'next-auth/react';
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
import UploadFileModal from "@/components/newProjectForm/UploadFileModal";
import {AlertCircle} from "lucide-react";
import {cn} from "@/lib/utils";

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
    industry: z.enum(["Cosmetics", "Leaflets", "Medical_Devices"], {
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
        path: ["destinationLanguage"],
    }
);

type FormData = z.infer<typeof formSchema>;

const industryOptions = [
    {value: "Cosmetics", label: "Cosmetics"},
    {value: "Leaflets", label: "Leaflets"},
    {value: "Medical_Devices", label: "Medical Devices"}
];

const languageOptions = [
    {value: "en", label: "English"},
    {value: "he", label: "Hebrew"},
    {value: "ar", label: "Arabic"}
];

type FormFieldConfig = {
    name: keyof FormData;
    label: string;
    type: 'input' | 'textarea' | 'select';
    placeholder?: string;
    options?: Array<{ value: string; label: string }>;
    required?: boolean;
};

export default function NewProjectForm() {
    const router = useRouter();
    const {data: session} = useSession();
    const currentUser = session?.userData
    const [showUploadModal, setShowUploadModal] = useState(false)
    const [isSubmitting, setIsSubmitting] = useState(false)
    const [selectedFile, setSelectedFile] = useState<File | null>(null)

    const form = useForm<FormData>({
        resolver: zodResolver(formSchema),
        mode: 'onChange',
        defaultValues: {
            name: '',
            description: '',
            industry: undefined,
            sourceLanguage: undefined,
            destinationLanguage: undefined,
            referenceFile: ''
        },
    });

    const formFields: FormFieldConfig[] = useMemo<FormFieldConfig[]>(() => [
        {
            name: 'name',
            label: 'Project Name',
            type: 'input' as const,
            placeholder: 'Enter project name',
            required: true,
        },
        {
            name: 'description',
            label: 'Description',
            type: 'textarea' as const,
            placeholder: 'Enter project description',
            required: true,
        },
        {
            name: 'industry',
            label: 'Industry',
            type: 'select' as const,
            options: industryOptions,
            required: true,
        },
    ], []);

    const languageFields: FormFieldConfig[] = useMemo<FormFieldConfig[]>(() => [
        {
            name: 'sourceLanguage',
            label: 'Source Language',
            type: 'select' as const,
            options: languageOptions.filter(lang => lang.value !== 'ar'),
            required: true,
        },
        {
            name: 'destinationLanguage',
            label: 'Target Language',
            type: 'select' as const,
            options: languageOptions,
            required: true,
        },
    ], [])

    const handleUpload = (files: File[]) => {
        if (files.length > 0) {
            setSelectedFile(files[0])
            form.setValue('referenceFile', files[0].name)
            setShowUploadModal(false)
        }
    }

    const onSubmit = useCallback(async (data: FormData) => {

        if (!selectedFile) {
            toast.error('Please select a reference file');
            return;
        }

        setIsSubmitting(true);

        try {
            if (!currentUser) {
                throw new Error('User not found');
            }

            const newProject = await createNewProject({
                ...data,
                currentUser
            });

            const isSaved = await saveNewProject(newProject);

            if (isSaved) {
                toast.success('Project created successfully');
                router.back();
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
    }, [selectedFile, currentUser, router]);

    return (
        <Card className="w-full max-w-md">
            <CardHeader>
                <CardTitle className="text-center">Project Details</CardTitle>
            </CardHeader>
            <CardContent>
                <ProjectForm {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                        {formFields.map((field: FormFieldConfig) => (
                            <FormField
                                key={field.name}
                                {...field}
                            />
                        ))}

                        <div className="grid grid-cols-2 gap-4">
                            {languageFields.map((field: FormFieldConfig) => (
                                <FormField
                                    key={field.name}
                                    {...field}
                                />
                            ))}
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
    );
}

