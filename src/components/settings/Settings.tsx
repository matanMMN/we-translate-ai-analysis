import React from 'react';
import {
    Container,
    Typography,
    Divider,
} from '@mui/material';
import Notifications from "@/components/settings/Notifications";
import Privacy from "@/components/settings/Privacy";
import Accessibility from "@/components/settings/Accessibility";
import AccountSettings from "@/components/settings/AccountSettings";
import LanguageSettings from "@/components/settings/Language";

export default function Settings() {

    return (
        <Container maxWidth="md" className="p-14">
            <Typography variant="h3" gutterBottom>Settings</Typography>
            <Divider/>
            <AccountSettings/>
            <Notifications/>
            <LanguageSettings/>
            <Privacy/>
            <Accessibility/>
        </Container>
    );
};


