"use client"

import {Divider, List, ListItem, ListItemText, Typography} from "@mui/material";
import React from "react";

export default function AccountSettings() {
    return (<>
        <Typography variant="h4" gutterBottom style={{marginTop: '20px'}}>Account Settings</Typography>
        <List>
            <ListItem>
                <ListItemText primary="Username" secondary="example_user"/>
            </ListItem>
            <ListItem>
                <ListItemText primary="Email" secondary="example@example.com"/>
            </ListItem>
        </List>
        <Divider/>
    </>)
}