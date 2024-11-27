import React, {ReactNode} from "react";
import {FormControl, FormField, FormItem, FormMessage} from "@/components/ui/form";
import {InputAdornment, TextField} from "@mui/material";
import {User} from 'lucide-react'
import {UseFormReturn} from "react-hook-form";

export default function FullNameInput({form}: { form: UseFormReturn<{ name?: string; email?: string; password?: string; confirmPassword?: string }>; }): ReactNode {
    return (
        <FormField
            control={form.control}
            name="name"
            render={({field}) => (
                <FormItem>
                    <FormControl>
                        <TextField
                            {...field}
                            margin="normal"
                            fullWidth
                            id="name"
                            label="Enter Full Name"
                            name="name"
                            autoComplete="name"
                            autoFocus
                            slotProps={{
                                input: {
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <User/>
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