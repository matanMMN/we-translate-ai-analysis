"use client"

import {Divider, List, ListItem, ListItemText, Typography} from "@mui/material";
import React from "react";

export default function LanguageSettings() {
    return (
        <>
            <Typography variant="h4" gutterBottom style={{marginTop: '20px'}}>Language Preferences</Typography>
            <List>
                <ListItem>
                    <ListItemText primary="Hebrew" secondary={"English"}/>
                </ListItem>
            </List>
            <Divider/>
        </>
    )
}