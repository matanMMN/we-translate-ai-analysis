"use client"

import React, {ReactNode} from "react";
import {Button} from "@mui/material";
import {useFormStatus} from "react-dom";

export default function LoginSubmit(): ReactNode {

    const {pending} = useFormStatus();

    return (
        <Button
            disabled={pending}
            type="submit"
            fullWidth
            variant="contained"
            sx={{mt: 3, mb: 2, backgroundColor: '#1f3d39'}}
        >
            {pending ? 'Logging in...' : 'Log in'}
        </Button>
    )
}