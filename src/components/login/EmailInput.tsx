import React, {ReactNode} from "react";
import {FormControl, FormField, FormItem, FormMessage} from "@/components/ui/form";
import {InputAdornment, TextField} from "@mui/material";
import MailOutlineIcon from "@mui/icons-material/MailOutline";
import {FormProps} from "@/components/login/form.interface";

export default function EmailInput({form}: FormProps): ReactNode {
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
                                            <MailOutlineIcon/>
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