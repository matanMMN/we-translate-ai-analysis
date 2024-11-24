"use client"

import React from "react";
import {Divider, List, ListItem, ListItemSecondaryAction, ListItemText, Switch, Typography} from "@mui/material";

export default function Notifications() {
    const [notification, setNotification] = React.useState(true);

    return (
        <>
            <Typography variant="h4" gutterBottom style={{marginTop: '20px'}}>Notification Preferences</Typography>
            <List>
                <ListItem>
                    <ListItemText primary="Email Alerts"/>
                    <ListItemSecondaryAction>
                        <Switch
                            edge="end"
                            onChange={() => setNotification(!notification)}
                            checked={notification}
                        />
                    </ListItemSecondaryAction>
                </ListItem>
            </List>
            <Divider/>
        </>
    )
}