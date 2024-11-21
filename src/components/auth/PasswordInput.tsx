import React, {ReactNode} from "react";
import {FormControl, FormField, FormItem, FormMessage} from "@/components/ui/form";
import {InputAdornment, TextField} from "@mui/material";
import LockIcon from "@mui/icons-material/Lock";
import {UseFormReturn} from "react-hook-form";


export default function PasswordInput({form}: {
    form: UseFormReturn<{ email: string; password: string; }>;
}): ReactNode {
    return (
        <FormField
            control={form.control}
            name="password"
            render={({field}) => (
                <FormItem>
                    <FormControl>
                        <TextField
                            {...field}
                            margin="normal"
                            fullWidth
                            name="password"
                            label="Enter password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
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
