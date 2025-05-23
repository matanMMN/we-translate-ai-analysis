import React, {ReactNode} from "react";
import {FormControl, FormField, FormItem, FormMessage} from "@/components/ui/form";
import {InputAdornment, TextField} from "@mui/material";
import {LockIcon} from 'lucide-react'
import {UseFormReturn} from "react-hook-form";


export default function PasswordInput({form, isConfirmPassword}: {
    form: UseFormReturn<{ name: string; email: string; password: string; confirmPassword: string}>, isConfirmPassword?: boolean;
}): ReactNode {

    const name = isConfirmPassword ? 'confirmPassword' : 'password';

    return (
        <FormField
            control={form.control}
            name={name}
            render={({field}) => (
                <FormItem>
                    <FormControl>
                        <TextField
                            {...field}
                            margin="normal"
                            fullWidth
                            name={name}
                            label={`${isConfirmPassword ? 'Enter password again' : 'Enter password'}`}
                            type="password"
                            id={name}
                            // autoComplete="current-password"
                            slotProps={{
                                input: {
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <LockIcon/>
                                        </InputAdornment>
                                    ),
                                },
                            }}
                        />
                    </FormControl>
                    <FormMessage/>
                </FormItem>
            )}
        />
    )
}
