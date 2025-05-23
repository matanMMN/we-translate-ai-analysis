"use client"

import React, {ReactNode} from "react";
import {Button} from "@mui/material";
import {useFormStatus} from "react-dom";
import LoadingLogoGif from "@/components/LoadingLogoGif";

export default function AuthSubmit({isRegister}: { isRegister?: boolean }): ReactNode {

    const {pending} = useFormStatus();


    return pending ? <LoadingLogoGif/> :
        <Button
            disabled={pending}
            type="submit"
            fullWidth
            variant="contained"
            sx={{mt: 3, mb: 2, backgroundColor: '#1f3d39'}}
        >{`${isRegister ? "Sign up" : "Log in"}`}
        </Button>


}