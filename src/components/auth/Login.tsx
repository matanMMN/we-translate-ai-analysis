import React from 'react';
import {
    Box,
    Grid,
    Paper,
    Typography,
} from '@mui/material';
import LoginForm from "@/components/auth/LoginForm";


export default async function Login() {
    return (
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
    );
};

