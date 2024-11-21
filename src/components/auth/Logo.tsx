"use client"

import {Box, CssBaseline, Grid, Typography} from "@mui/material";
import Image from "next/image";
import Logo from '@/assets/icon.png';
import React from "react";

export default function LogoComponent() {
    return (
        <>
            <CssBaseline/>
            <Grid
                item
                xs={false}
                sm={4}
                md={7}
                sx={{
                    backgroundColor: '#1f3d39',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    color: 'white'
                }}
            >
                <Box sx={{display: 'flex', alignItems: 'center'}}>
                    <Image src={Logo} alt="MediTranslate AI" style={{width: '150px', marginRight: '20px'}}/>
                    <Typography component="h1" variant="h1" align="center" style={{
                        userSelect: "none"
                    }}>
                        MediTranslate AI
                    </Typography>
                </Box>
            </Grid>
        </>
    )
}