import React from 'react';
import {
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
        <div className="container h-dvh max-h-[calc(100%-10px)] px-14 overflow-y-auto flex flex-col">
            <Typography variant="h3" gutterBottom>Settings</Typography>
            <Divider/>
            <AccountSettings/>
            <Notifications/>
            <LanguageSettings/>
            <Privacy/>
            <Accessibility/>
        </div>
    );
};


