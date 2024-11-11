"use client"
import {Divider, List, ListItem, ListItemSecondaryAction, ListItemText, Switch, Typography} from "@mui/material";
import React from "react";

export default function Privacy() {

    const [privacy, setPrivacy] = React.useState(true);

    return (
        <>
            <Typography variant="h4" gutterBottom style={{marginTop: '20px'}}>Privacy Settings</Typography>
            <List>
                <ListItem>
                    <ListItemText primary="Profile Visibility"/>
                    <ListItemSecondaryAction>
                        <Switch
                            edge="end"
                            onChange={() => setPrivacy(!privacy)}
                            checked={privacy}
                        />
                    </ListItemSecondaryAction>
                </ListItem>
            </List>
            <Divider/>
        </>
    )
}