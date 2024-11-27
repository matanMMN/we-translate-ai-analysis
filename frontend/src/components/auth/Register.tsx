'use client'
import {
    Box,
    Grid,
    Paper
} from '@mui/material';
import Link from 'next/link'
import {Form} from "@/components/ui/form";
import EmailInput from "@/components/auth/EmailInput";
import PasswordInput from "@/components/auth/PasswordInput";
import AuthSubmit from "@/components/auth/AuthSubmit";
import {useRouter} from "next/navigation";
import {useForm, UseFormReturn} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import * as z from "zod";
import FullNameInput from "@/components/auth/FullNameInput";
import {signUp} from "@/actions/signUp";
import {toast} from "sonner";

const FormSchema = z.object({
    // email: z.string().trim().email({message: "EmailInput is invalid"}), // Production validation
    // password: z.string().trim().min(8, {message: "Password is invalid"}) // Production validation
    name: z.string().trim().min(1, {message: "Name is invalid"}),
    email: z.string().trim().email({message: "EmailInput is invalid"}), // Production validation
    password: z.string().trim().min(1, {message: "Password is invalid"}),
    confirmPassword: z.string().trim().min(1, {message: "Password confirmation is invalid"})
}).refine(data => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
})
type FormData = z.infer<typeof FormSchema>;

export default function Register() {

    const router = useRouter();

    const form: UseFormReturn<FormData> = useForm<FormData>({
        resolver: zodResolver(FormSchema),
        defaultValues: {
            name: '',
            email: '',
            password: '',
            confirmPassword: ''
        }
    });

    const onSubmit = async (data: FormData) => {

        const res = await signUp(data)
        if (res?.success) {
            toast.success("Account created successfully")
            router.replace('/login')
        } else
            toast.error("User already exists")
    };
    return (
        <Grid
            item
            xs={12}
            sm={8}
            md={5}
            component={Paper}
            elevation={6}
            square
            sx={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center'
            }}
        >
            <Box
                sx={{
                    my: 8,
                    mx: 4,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    width: '100%',
                    maxWidth: '400px',
                }}
            >
                <Form {...form}>
                    <div className="space-y-2">
                        <h1 className="text-2xl font-semibold tracking-tight">Create an account</h1>
                        <p className="text-sm text-muted-foreground">
                            Already have an account?{' '}
                            <Link href="/login" className="text-[#1F3B33] hover:underline">
                                Log in
                            </Link>
                        </p>
                    </div>

                    <form onSubmit={form.handleSubmit(onSubmit)} className={"w-full"}>
                        <FullNameInput form={form}/>
                        <EmailInput form={form}/>
                        <PasswordInput form={form}/>
                        <PasswordInput form={form} isConfirmPassword/>
                        <AuthSubmit isRegister/>
                    </form>
                </Form>
            </Box>
        </Grid>
    )
}