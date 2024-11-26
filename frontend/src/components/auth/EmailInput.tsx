import React, {ReactNode} from "react";
import {FormControl, FormField, FormItem, FormMessage} from "@/components/ui/form";
import {InputAdornment, TextField} from "@mui/material";
import {Mail} from 'lucide-react'
import {UseFormReturn} from "react-hook-form";

export default function EmailInput({form}: { form: UseFormReturn<{ email: string; password: string; }>; }): ReactNode {
    return (
        <FormField
            control={form.control}
            name="email"
            render={({field}) => (
                <FormItem>
                    <FormControl>
                        <TextField
                            {...field}
                            margin="normal"
                            fullWidth
                            id="username"
                            label="Enter email"
                            name="username"
                            autoComplete="username"
                            autoFocus
                            slotProps={{
                                input: {
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <Mail/>
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