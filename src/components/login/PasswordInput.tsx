import React, {ReactNode} from "react";
import {FormControl, FormField, FormItem, FormMessage} from "@/components/ui/form";
import {InputAdornment, TextField} from "@mui/material";
import {FormProps} from "@/components/login/form.interface";
import LockIcon from "@mui/icons-material/Lock";


export default function PasswordInput({form}: FormProps): ReactNode {
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
