"use client"

import React, {ReactNode, useEffect, useState} from "react";
import {Form} from "@/components/ui/form";
import {Checkbox, FormControlLabel, Grid, Typography} from "@mui/material";
import * as z from "zod";
import {useForm, UseFormReturn} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import EmailInput from "@/components/auth/EmailInput";
import LoginSubmit from "@/components/auth/LoginSubmit";
import PasswordInput from "@/components/auth/PasswordInput";
import {signIn, SignInResponse, useSession} from "next-auth/react";
import {useRouter} from "next/navigation";
import {writeToStorage} from "@/lib/storage";

const FormSchema = z.object({
    // email: z.string().trim().email({message: "EmailInput is invalid"}), // Production validation
    // password: z.string().trim().min(8, {message: "Password is invalid"}) // Production validation
    email: z.string().trim().min(1, {message: "EmailInput is invalid"}),
    password: z.string().trim().min(1, {message: "Password is invalid"})
});
type FormData = z.infer<typeof FormSchema>;

export default function LoginForm(): ReactNode {


    const {data: session} = useSession();
    const router = useRouter();
    const [error, setError] = useState<string | null | undefined>(null);

    useEffect(() => {
        if (session && session?.accessToken) {
            writeToStorage("access_token", session?.accessToken);
        }
    }, [session]);


    const form: UseFormReturn<FormData> = useForm<FormData>({
        resolver: zodResolver(FormSchema),
        defaultValues: {
            email: '',
            password: ''
        }
    });

    const onSubmit = async (data: FormData) => {
        const {email, password} = data;
        const res: SignInResponse | undefined = await signIn('credentials', {
            email,
            password,
            redirect: false,
            callbackUrl: '/'
        });
        if (res?.ok)
            router.replace('/')
        else
            setError(res?.error)
    };


    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className={"w-full"}>
                <EmailInput form={form}/>
                <PasswordInput form={form}/>
                <div className="flex font-bold text-red-500">{error || ""}</div>
                <Grid container justifyContent="space-between">
                    <FormControlLabel control={<Checkbox value="remember" color="primary"/>}
                                      label="Remember me"/>
                    <Typography className={"underline"} component="a" href="" variant="body2"
                                sx={{alignSelf: 'center'}}>
                        Forgot password?
                    </Typography>
                </Grid>
                <LoginSubmit/>
            </form>
        </Form>
    )
}