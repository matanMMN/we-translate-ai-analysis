"use client"
import React from 'react';
import {supportedSourceLanguages, supportedTargetLanguages} from '@/config/constants'
import UploadFileModal from './UploadFileModal';
import * as z from "zod";
import {useForm, UseFormReturn} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import checkIfProjectExists from "@/actions/UtilActions";
import {FormField, FormItem, Form, FormLabel, FormControl} from "@/components/ui/form";
import {Paperclip} from "lucide-react"
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card"
import {Input} from "@/components/ui/input"
import {Button} from "@/components/ui/button"
import {Textarea} from "@/components/ui/textarea"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

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

    // const dispatch = useDispatch();
    // const [file, setFile] = useState(null);

    const [showUploadModal, setShowUploadModal] = React.useState(false)

    const handleUpload = (files: File[]) => {
        // Handle the uploaded files here
        console.log('Uploaded files:', files)
    }

    // const onFileChange = (f: React.SetStateAction<null>) => {
    //     setFile(f)
    // }

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


    const handleSubmit = async (data: FormData) => {
        console.log(data)
    };


    return (
        <div className="min-w-[28rem]">
            <Card className="w-full max-w-md mx-auto">
                <CardHeader>
                    <CardTitle className="text-center">Project Details</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4 flex flex-col">
                    <div className="space-y-4">
                        <Form {...form} >
                            <form className="space-y-4" onSubmit={form.handleSubmit(handleSubmit)}>
                                <FormField
                                    control={form.control}
                                    name={"name"}
                                    render={({field}) => (
                                        <FormItem className="w-full">
                                            <FormControl className="w-full">
                                                <Input placeholder="Name" {...field}
                                                       className="bg-gray-50 border-gray-200  flex h-9 w-full rounded-md border border-input px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                                                />
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
                                                <Textarea placeholder="Description" {...field}
                                                          className="bg-gray-50 border-gray-200 min-h-[80px]"/>
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
                                                <Select>
                                                    <SelectTrigger className="w-full bg-gray-50 border-gray-200">
                                                        <SelectValue placeholder="Industry"/>
                                                    </SelectTrigger>
                                                    <SelectContent {...field}>
                                                        <SelectItem value="workspace1">Cosmetics</SelectItem>
                                                        <SelectItem value="workspace2">Leaflets</SelectItem>
                                                        <SelectItem value="workspace3">Medical Devices</SelectItem>
                                                    </SelectContent>
                                                </Select>

                                            </FormControl>
                                        </FormItem>
                                    )}>
                                </FormField>


                                <div className="grid grid-cols-2 gap-4">
                                    <FormField
                                        control={form.control}
                                        name={"sourceLanguage"}
                                        render={({field}) => (
                                            <FormItem className="w-full">
                                                <FormLabel></FormLabel>
                                                <FormControl className="w-full">

                                                    <Select>
                                                        <SelectTrigger className="w-full bg-gray-50 border-gray-200">
                                                            <SelectValue placeholder="Source language"/>
                                                        </SelectTrigger>
                                                        <SelectContent {...field}>
                                                            <SelectItem value="en">English</SelectItem>
                                                            <SelectItem value="he">Hebrew</SelectItem>
                                                        </SelectContent>
                                                    </Select>

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

                                                    <Select>
                                                        <SelectTrigger className="w-full bg-gray-50 border-gray-200">
                                                            <SelectValue placeholder="Target language"/>
                                                        </SelectTrigger>
                                                        <SelectContent {...field}>
                                                            <SelectItem value="en">English</SelectItem>
                                                            <SelectItem value="he">Hebrew</SelectItem>
                                                            <SelectItem value="ar">Arabic</SelectItem>
                                                        </SelectContent>
                                                    </Select>

                                                </FormControl>
                                            </FormItem>
                                        )}>
                                    </FormField>
                                </div>
                                <Button
                                    variant="outline"
                                    className="w-full bg-gray-50 border-gray-200 hover:bg-gray-100 hover:text-gray-900"
                                    onClick={() => setShowUploadModal(true)}
                                >
                                    <Paperclip className="w-4 h-4 mr-2"/>
                                    Add reference file
                                </Button>
                                <Button className="w-full bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white">
                                    Start a Project
                                </Button>
                            </form>
                        </Form>
                    </div>
                </CardContent>
            </Card>
            <UploadFileModal
                open={showUploadModal}
                onClose={() => setShowUploadModal(false)}
                onUpload={handleUpload}
            />
        </div>
    )

    // return (
    //     <div
    //         className=" rounded-lg shadow-xl w-[600px] h-[500px] max-w-md bg-white p-12 flex flex-col justify-center content-center items-center">
    //         <Form {...form}>
    //             <form onSubmit={form.handleSubmit(handleSubmit)}
    //                   className="space-y-4 w-full flex flex-col justify-center content-center items-center">
    //                 <span className="font-bold text-3xl text-center w-full">Project Details</span>
    //
    //                 <FormField
    //                     control={form.control}
    //                     name={"name"}
    //                     render={({field}) => (
    //                         <FormItem className="w-full">
    //                             {/*<FormLabel>Name</FormLabel>*/}
    //                             <FormControl className="w-full">
    //                                 <Input placeholder="Name" {...field} className="w-full bg-[#F0F2F5]"/>
    //                             </FormControl>
    //                         </FormItem>
    //                     )}>
    //                 </FormField>
    //
    //                 <FormField
    //                     control={form.control}
    //                     name={"description"}
    //                     render={({field}) => (
    //                         <FormItem className="w-full">
    //                             <FormLabel></FormLabel>
    //                             <FormControl className="w-full">
    //                                 <Input placeholder="Description" {...field} className="w-full bg-[#F0F2F5]"/>
    //                             </FormControl>
    //                         </FormItem>
    //                     )}>
    //                 </FormField>
    //
    //                 <FormField
    //                     control={form.control}
    //                     name={"industry"}
    //                     render={({field}) => (
    //                         <FormItem className="w-full">
    //                             <FormLabel></FormLabel>
    //                             <FormControl className="w-full">
    //                                 <Input placeholder="Industry" {...field} className="w-full bg-[#F0F2F5]"/>
    //                             </FormControl>
    //                         </FormItem>
    //                     )}>
    //                 </FormField>
    //
    //                 <FormField
    //                     control={form.control}
    //                     name={"sourceLanguage"}
    //                     render={({field}) => (
    //                         <FormItem className="w-full">
    //                             <FormLabel></FormLabel>
    //                             <FormControl className="w-full">
    //                                 <Input placeholder="Source language" {...field} className="w-full bg-[#F0F2F5]"/>
    //                             </FormControl>
    //                         </FormItem>
    //                     )}>
    //                 </FormField>
    //
    //                 <FormField
    //                     control={form.control}
    //                     name={"destinationLanguage"}
    //                     render={({field}) => (
    //                         <FormItem className="w-full">
    //                             <FormLabel></FormLabel>
    //                             <FormControl className="w-full">
    //                                 <Input placeholder="Target language" {...field} className="w-full bg-[#F0F2F5]"/>
    //                             </FormControl>
    //                         </FormItem>
    //                     )}>
    //                 </FormField>
    //
    //                 <FormField
    //                     control={form.control}
    //                     name={"referenceFile"}
    //                     render={({field}) => (
    //                         <FormItem className="w-full">
    //                             <FormLabel></FormLabel>
    //                             <FormControl className="w-full">
    //                                 <Input placeholder="Reference File" {...field} className="w-full bg-[#F0F2F5]"/>
    //                             </FormControl>
    //                         </FormItem>
    //                     )}>
    //                 </FormField>
    //
    //
    //                 <Button
    //                     type="submit"
    //                     variant="contained"
    //                     color="primary"
    //                     className={`w-full max-w-[400px] normal-case text-white border rounded-2xl bg-[${theme.colors.mainColor}]`}>
    //                     Start a Project
    //                 </Button>
    //             </form>
    //         </Form>
    //     </div>
    // )
};

