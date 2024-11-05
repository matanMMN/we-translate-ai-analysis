"use client"

import {useEffect, useRef, useState} from 'react';
import {DocumentEditorContainerComponent, Toolbar} from '@syncfusion/ej2-react-documenteditor';
import {TitleBar} from './TitleBar';
// import { useSelector } from 'react-redux';
// import { selectSession } from '@/store/slices/projectSlice';
import {EditorConfig} from './types';
import {handleFileLoad} from './handlers/fileHandler';
import {setupContextMenu} from './handlers/menuHandler';
import {handleAutoSave} from './handlers/autoSaveHandler';
import DocumentContainer from './DocumentContainer';
import { useRouter } from 'next/navigation';
import {useAppDispatch} from "@/hooks/useAppDispatch";


DocumentEditorContainerComponent.Inject(Toolbar);

export default function Editor({userSession, headerTitle, readOnly = false, closeButton = false}: EditorConfig) {

    const dispatch = useAppDispatch();
    const router = useRouter();
    const isInitialized = useRef(false);
    const contentChanged = useRef(false);
    const container = useRef<DocumentEditorContainerComponent>(null);
    const [docxHash, setDocxHash] = useState<string | null>(null);
    const [commentsHash, setCommentsHash] = useState<string | null>(null);
    const hostUrl = "https://services.syncfusion.com/react/production/api/documenteditor/";
    let titleBar: TitleBar;

    useEffect(() => {
        if (!isInitialized.current) {
            initializeEditor();
            isInitialized.current = true;
        }
    }, []);

    useEffect(() => {
        return handleAutoSave(container, contentChanged, docxHash, commentsHash, setDocxHash, setCommentsHash);
    }, [docxHash, commentsHash]);

    const initializeEditor = async () => {
        if (!container.current) return;

        window.onbeforeunload = () => "Want to save your changes?";
        container.current.documentEditor.pageOutline = "#E0E0E0";
        container.current.documentEditor.acceptTab = true;
        container.current.documentEditor.resize();

        titleBar = new TitleBar(
            document.getElementById(`documenteditor_titlebar`),
            container.current.documentEditor,
            true
        );

        await handleFileLoad(container, userSession, headerTitle, titleBar);

        if (!readOnly) {
            setupContextMenu(container, dispatch, router.push);
        }

        // Set toolbar items based on mode
        if (readOnly) {
            container.current.documentEditor.isReadOnly = true;
            container.current.documentEditor.enableContextMenu = false;
            container.current.resize();
            const downloadButton = document.getElementById("documenteditor-share") as HTMLButtonElement | null;
            if (downloadButton) {
                downloadButton.style.display = "none";
            }
            container.current.toolbarItems = ['Open', 'Separator', 'Find'];
        }

        if (closeButton) {
            const XButton = document.getElementById("de-close") as HTMLButtonElement | null;
            if (XButton)
                XButton.style.display = "block";
        }

        container.current.contentChange = () => {
            contentChanged.current = true;
        };
    };

    return (
        <div id="documenteditor_container_body">
            <div className="control-pane">
                <div className="control-section">
                    <div id="documenteditor_titlebar" className="e-de-ctn-title"/>
                    <DocumentContainer container={container} hostUrl={hostUrl}/>
                </div>
            </div>
        </div>
    );
}
