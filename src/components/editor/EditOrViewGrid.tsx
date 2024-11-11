"use client"

import {Button} from "@/components/ui/button";
import * as React from "react";
import {useRef, useState} from 'react';
import {DialogComponent} from '@syncfusion/ej2-react-popups';
import {DocumentEditorContainerComponent, Toolbar} from '@syncfusion/ej2-react-documenteditor';
import Editor from "@/components/editor/Editor";

DocumentEditorContainerComponent.Inject(Toolbar);

export default function EditOrViewGrid() {

    const dialogInstance = useRef<DialogComponent>(null);
    const [isDialogOpen, setDialogOpen] = useState(false);
    const [isView, setIsView] = useState(false);

    const dialogClose = (): void => {
        setDialogOpen(false);
    }

    const dialogOpen = (): void => {
        setDialogOpen(true);
    }


    const onViewClick = async () => {
        setIsView(true)
        setDialogOpen(true);
    }

    const onEditClick = async () => {
        setIsView(false)
        setDialogOpen(true);
    }
    return (
        <>
            <DialogComponent id="defaultDialog" ref={dialogInstance} isModal={true} visible={isDialogOpen}
                             style={{padding: "1rem"}}
                             width={'90%'} height={'90%'} zIndex={1500} open={dialogOpen} close={dialogClose}>
                {isDialogOpen && <Editor readOnly={isView} closeButton={true} dialogRef={dialogInstance}/>}
            </DialogComponent>

            <div className="grid grid-cols-2 gap-4">
                <Button
                    onClick={onEditClick}
                    className="bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white"
                >
                    Edit Project
                </Button>
                <Button
                    onClick={onViewClick}
                    className="bg-[#1D3B34] hover:bg-[#1D3B34]/90 text-white"
                >
                    View Project
                </Button>
            </div>
        </>
    )
}