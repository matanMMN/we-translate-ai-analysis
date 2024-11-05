"use client"

import {Button} from "@/components/ui/button";
import * as React from "react";
import {useEffect, useRef, useState} from 'react';
import {DialogComponent} from '@syncfusion/ej2-react-popups';
import {DocumentEditorContainerComponent, Toolbar} from '@syncfusion/ej2-react-documenteditor';
import {TitleBar} from '@/components/editor/TitleBar';
import * as data from '@/app/(content)/[projectId]/editor/data-default.json';
import {Session} from "next-auth";

DocumentEditorContainerComponent.Inject(Toolbar);

export default function EditOrViewGrid({userSession}: { userSession: Session | null }) {

    const dialogInstance = useRef<DialogComponent>(null);
    const [isDialogOpen, setDialogOpen] = useState(false);
    const hostUrl: string = "https://services.syncfusion.com/react/production/api/documenteditor/";
    const container = useRef<DocumentEditorContainerComponent>(null);
    let titleBar: TitleBar;

    useEffect(() => {
        window.onbeforeunload = function () {
            return "Want to save your changes?";
        };
        container.current.documentEditor.pageOutline = "#E0E0E0";
        container.current.documentEditor.acceptTab = true;
        container.current.documentEditor.resize();
        if (!titleBar) {
            titleBar = new TitleBar(
                document.getElementById("documenteditor_titlebar"),
                container.current.documentEditor,
                true, false, dialogInstance.current
            );
        }
        onLoadDefault();
    }, []);


    const onLoadDefault = (): void => {
        titleBar.updateDocumentTitle();
        container.current!.documentEditor.currentUser = `${userSession?.userData?.first_name} ${userSession?.userData?.last_name}`
        container.current.documentChange = (): void => {
            titleBar.updateDocumentTitle();
            container.current.documentEditor.focusIn();
        };
    };

    const dialogClose = (): void => {
        setDialogOpen(false);
    }

    const dialogOpen = (): void => {
        setDialogOpen(true);
        container.current.documentEditor.resize();
    }


    const onViewClick = (args): void => {
        setDialogOpen(true);
        container.current.documentEditor.open(JSON.stringify(data));
        container.current.documentEditor.isReadOnly = true;
        container.current.documentEditor.enableContextMenu = false;
        container.current.resize();
        const downloadButton = document.getElementById("documenteditor-share") as HTMLButtonElement | null;
        if (downloadButton) {
            downloadButton.style.display = "none";
        }
        const closeButton = document.getElementById("de-close") as HTMLButtonElement | null;
        if (closeButton) {
            closeButton.style.display = "block";
        }
        // container.current.documentEditor.documentName = args.rowData.FileName.replace(".docx", "");
        document.getElementById("documenteditor_title_name").textContent = container.current.documentEditor.documentName;
        container.current.toolbarItems = ['Open', 'Separator', 'Find'];
    }

    const onEditClick = (args): void => {
        setDialogOpen(true);
        container.current.documentEditor.open(JSON.stringify(data));
        container.current.documentEditor.isReadOnly = false;
        container.current.documentEditor.enableContextMenu = true;
        container.current.resize();
        const downloadButton = document.getElementById("documenteditor-share") as HTMLButtonElement | null;
        if (downloadButton) {
            downloadButton.style.display = "block";
        }
        const closeButton = document.getElementById("de-close") as HTMLButtonElement | null;
        if (closeButton) {
            closeButton.style.display = "block";
        }
        // container.current.documentEditor.documentName = args.rowData.FileName.replace(".docx", "");
        document.getElementById("documenteditor_title_name").textContent = container.current.documentEditor.documentName;
        container.current.toolbarItems = ['New', 'Open', 'Separator', 'Undo', 'Redo', 'Separator', 'Image', 'Table', 'Hyperlink', 'Bookmark', 'TableOfContents', 'Separator', 'Header', 'Footer', 'PageSetup', 'PageNumber', 'Break', 'InsertFootnote', 'InsertEndnote', 'Separator', 'Find', 'Separator', 'Comments', 'TrackChanges', 'Separator', 'LocalClipboard', 'RestrictEditing', 'Separator', 'FormFields', 'UpdateFields'];
    }
    return (
        <>
            <DialogComponent id="defaultDialog" ref={dialogInstance} isModal={true} visible={isDialogOpen}
                             width={'90%'} height={'90%'} zIndex={1500} open={dialogOpen} close={dialogClose}>
                <div>
                    <div id="documenteditor_titlebar" className="e-de-ctn-title"></div>
                    <div id="documenteditor_container_body">
                        <DocumentEditorContainerComponent showPropertiesPane={false}
                                                          id="container" height='780px'
                                                          ref={container}
                                                          style={{display: "block"}}
                                                          serviceUrl={hostUrl}
                                                          zIndex={3000}
                                                          enableToolbar={true}
                                                          locale="en-US"
                        />
                    </div>
                </div>
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