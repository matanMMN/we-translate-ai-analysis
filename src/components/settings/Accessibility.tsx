"use client"

import {List, ListItem, ListItemSecondaryAction, ListItemText, Switch, Typography} from "@mui/material";
import React from "react";

export default function Accessbility() {
    const [accessibility, setAccessibility] = React.useState(false);

    return (
        <>
            <Typography variant="h4" gutterBottom style={{marginTop: '20px'}}>Accessibility Settings</Typography>
            <List>
                <ListItem>
                    <ListItemText primary="High Contrast Mode"/>
                    <ListItemSecondaryAction>
                        <Switch
                            edge="end"
                            onChange={() => setAccessibility(!accessibility)}
                            checked={accessibility}
                        />
                    </ListItemSecondaryAction>
                </ListItem>
            </List>
        </>
    )
}