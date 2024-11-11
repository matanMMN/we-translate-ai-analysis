import React from 'react';
import {
    Box,
    CssBaseline,
    Grid,
    Paper,
    Typography,
} from '@mui/material';
import Logo from '@/assets/icon.png';
import Image from "next/image";
import LoginForm from "@/components/login/LoginForm";


export default async function Login() {


    return (
        <Grid container component="main" sx={{height: '100vh'}}>
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
            <Grid
                item
                xs={12}
                sm={8}
                md={5}
                component={Paper}
                elevation={6}
                square
                sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center'
                }}
            >
                <Box
                    sx={{
                        my: 8,
                        mx: 4,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        width: '100%',
                        maxWidth: '400px',
                    }}
                >
                    <Typography className={"my-2"} component="h1" variant="h5">
                        Log in
                    </Typography>
                    <LoginForm/>
                </Box>
            </Grid>
        </Grid>
    );
};

