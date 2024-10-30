"use client"
import React, {useEffect, useState} from 'react';
import {
    Button,
    Modal,
    TextField,
    Grid,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Typography,
    FormHelperText, Grid2
} from '@mui/material';
import {AttachFile} from '@mui/icons-material';
import {supportedSourceLanguages, supportedTargetLanguages} from '@/config/constants'
import {useDispatch, useSelector} from 'react-redux';
import UploadFileModal from './UploadFileModal';
import {selectTheme} from "@/store/slices/themeSlice";
import * as z from "zod";
import {useForm, UseFormReturn} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import checkIfProjectExists from "@/actions/UtilActions";
import {FormField, FormItem, Form, FormLabel} from "@/components/ui/form";
import {Input} from "@/components/ui/input";

const FormSchema = z.object({
    name: z.string().trim().min(1, {message: "Name is required"}).max(20, {message: "Name must be less than 20 characters"}).refine(async (name) => {
        const existingProject = await checkIfProjectExists(name);
        return !existingProject;
    }, {message: "Project name already exists"}),
    description: z.string().trim().min(1, {message: "Description is required"}).max(500, {message: "Description must be less than 500 characters"}),
    industry: z.enum(["Cosmetics", "Leaflets", "Medical Devices"], {message: "Industry must be one of Cosmetics, Leaflets, or Medical Devices"}),
    sourceLanguage: z.enum(supportedSourceLanguages, {message: "Source Language is required and must be one of the supported languages"}),
    destinationLanguage: z.enum(supportedTargetLanguages, {message: "Target Language is required and must be one of the supported languages"}),
    referenceFile: z.string().trim().min(1, {message: "Reference File is required"}).refine((file) => {
        const validExtensions = ["doc", "docx", "pdf"];
        const fileExtension = file.split('.').pop()?.toLowerCase();
        return fileExtension && validExtensions.includes(fileExtension);
    }, {message: "Reference File must be a valid doc, docx, or PDF file"}),
});

type FormData = z.infer<typeof FormSchema>;


export default function NewProjectForm() {

    const dispatch = useDispatch();
    const theme = useSelector(selectTheme)
    const [file, setFile] = useState(null);
    const onFileChange = (f: React.SetStateAction<null>) => {
        setFile(f)
    }

    const form: UseFormReturn<FormData> = useForm<FormData>({
        resolver: zodResolver(FormSchema),
        defaultValues: {
            name: '',
            description: '',
            industry: undefined,
            sourceLanguage: '',
            destinationLanguage: '',
            referenceFile: ''
        }
    });


    const handleSubmit = async (event) => {
        dispatch(
            createProject({
                workspaceNamespace: selectedWorkspace ? selectedWorkspace.namespace : workspace,
                title,
                description,
                sourceLanguage,
                targetLanguage,
                file
            })
        )
    };


    return (
        <div
            className=" rounded-lg shadow-xl w-[600px] h-[500px] max-w-md bg-white p-12 flex flex-col justify-center content-center items-center">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(handleSubmit)}
                      className="space-y-4 w-full flex flex-col justify-center content-center items-center">
                    <span className="font-bold text-3xl text-center w-full">Project Details</span>

                    <FormField
                        control={form.control}
                        name={"name"}
                        render={({field}) => (
                            <FormItem className="w-full">
                                {/*<FormLabel>Name</FormLabel>*/}
                                <FormControl className="w-full">
                                    <Input placeholder="Name" {...field} className="w-full bg-[#F0F2F5]"/>
                                </FormControl>
                            </FormItem>
                        )}>
                    </FormField>

                    <FormField
                        control={form.control}
                        name={"description"}
                        render={({field}) => (
                            <FormItem className="w-full">
                                <FormLabel></FormLabel>
                                <FormControl className="w-full">
                                    <Input placeholder="Description" {...field} className="w-full bg-[#F0F2F5]"/>
                                </FormControl>
                            </FormItem>
                        )}>
                    </FormField>

                    <FormField
                        control={form.control}
                        name={"industry"}
                        render={({field}) => (
                            <FormItem className="w-full">
                                <FormLabel></FormLabel>
                                <FormControl className="w-full">
                                    <Input placeholder="Industry" {...field} className="w-full bg-[#F0F2F5]"/>
                                </FormControl>
                            </FormItem>
                        )}>
                    </FormField>

                    <FormField
                        control={form.control}
                        name={"sourceLanguage"}
                        render={({field}) => (
                            <FormItem className="w-full">
                                <FormLabel></FormLabel>
                                <FormControl className="w-full">
                                    <Input placeholder="Source language" {...field} className="w-full bg-[#F0F2F5]"/>
                                </FormControl>
                            </FormItem>
                        )}>
                    </FormField>

                    <FormField
                        control={form.control}
                        name={"destinationLanguage"}
                        render={({field}) => (
                            <FormItem className="w-full">
                                <FormLabel></FormLabel>
                                <FormControl className="w-full">
                                    <Input placeholder="Target language" {...field} className="w-full bg-[#F0F2F5]"/>
                                </FormControl>
                            </FormItem>
                        )}>
                    </FormField>

                    <FormField
                        control={form.control}
                        name={"referenceFile"}
                        render={({field}) => (
                            <FormItem className="w-full">
                                <FormLabel></FormLabel>
                                <FormControl className="w-full">
                                    <Input placeholder="Reference File" {...field} className="w-full bg-[#F0F2F5]"/>
                                </FormControl>
                            </FormItem>
                        )}>
                    </FormField>


                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        className={`w-full max-w-[400px] normal-case text-white border rounded-2xl bg-[${theme.colors.mainColor}]`}>
                        Start a Project
                    </Button>
                </form>
            </Form>
        </div>
    )
};

