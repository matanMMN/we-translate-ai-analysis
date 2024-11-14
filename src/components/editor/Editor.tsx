"use client"

import {useCallback, useEffect, useRef, useState} from 'react';
import {DocumentEditorContainerComponent, Toolbar} from '@syncfusion/ej2-react-documenteditor';
import {TitleBar} from './TitleBar';
import {EditorConfig} from './types';
import {handleFileLoad} from './handlers/fileHandler';
import {setupContextMenu} from './handlers/menuHandler';
import {useAutoSave} from './handlers/autoSaveHandler';
import DocumentContainer from './DocumentContainer';
import {useRouter} from 'next/navigation';
import {useAppDispatch} from "@/hooks/useAppDispatch";
import {useAppSelector} from "@/hooks/useAppSelector";
import {selectSession} from "@/store/slices/sessionSlice";
import {Project} from "@/lib/userData";


DocumentEditorContainerComponent.Inject(Toolbar);

export default function Editor({
                                   readOnly = false,
                                   closeButton = false,
                                   // projectId,
                                   dialogRef
                               }: EditorConfig) {

    const project = useAppSelector(selectSession)
    const {userSession, projectId} = project;
    const {title: headerTitle} = project.project as Project
    const dispatch = useAppDispatch();
    const router = useRouter();
    const isInitialized = useRef(false);
    const contentChanged = useRef(false);
    const container = useRef<DocumentEditorContainerComponent>(null);
    const [docxHash, setDocxHash] = useState<string | null>(null);
    const [commentsHash, setCommentsHash] = useState<string | null>(null);
    const hostUrl = "https://services.syncfusion.com/react/production/api/documenteditor/";
    const sourceLanguage = "he";
    let titleBar: TitleBar;

    useAutoSave(container, docxHash, commentsHash, setDocxHash, setCommentsHash);


    const initializeEditor = useCallback(async () => {
        if (!container.current) return;

        window.onbeforeunload = () => "Want to save your changes?";
        container.current.documentEditor.pageOutline = "#E0E0E0";
        container.current.documentEditor.acceptTab = true;
        container.current.documentEditor.resize();

        titleBar = new TitleBar(
            document.getElementById(`documenteditor_titlebar`),
            container.current.documentEditor,
            true,
            false,
            dialogRef && dialogRef.current!
        );

        await handleFileLoad(container, userSession, projectId!, headerTitle, titleBar);

        if (!readOnly) {
            document.getElementById("defaultDialog_dialog-content")?.remove()
            setupContextMenu({
                container,
                dispatch,
                navigate: router.push,
                projectId,
                sourceLanguage
            });
        }

        // Set toolbar items based on mode
        if (readOnly) {
            container.current.documentEditor.isReadOnly = true;
            container.current.documentEditor.enableContextMenu = false;
            document.getElementById("defaultDialog_dialog-content")?.remove()
            // container.current.resize();
            const downloadButton = document.getElementById("documenteditor-share") as HTMLButtonElement | null;
            if (downloadButton) {
                downloadButton.style.display = "none";
            }
            container.current.toolbarItems = ['Find'];
        }

        if (closeButton) {
            const XButton = document.getElementById("de-close") as HTMLButtonElement | null;
            if (XButton)
                XButton.style.display = "block";
        }

        container.current.contentChange = () => {
            contentChanged.current = true;
        };
    }, []);

    useEffect(() => {
        if (!isInitialized.current) {
            initializeEditor();
            isInitialized.current = true;
            console.log("Editor initialized");
        }
    }, [initializeEditor]);

    return (
        <div id="documenteditor_container_body">
            <div className="control-pane">
                <div className="control-section">
                    <div id="documenteditor_titlebar" className="e-de-ctn-title"/>
                    <DocumentContainer container={container} hostUrl={hostUrl} isView={readOnly}/>
                </div>
            </div>
        </div>
    );
}
