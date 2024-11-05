"use client"

import * as React from 'react';
import {useEffect, useRef, useState} from 'react';
import {DocumentEditorContainerComponent, Toolbar} from '@syncfusion/ej2-react-documenteditor';
import {TitleBar} from './TitleBar';
import * as data from '@/app/(content)/[projectId]/editor/data-default.json';
import {Session} from "next-auth";
import {handleEditorChanges, srcFile} from "@/actions/EditorChanges";
import {MenuItemModel} from "@syncfusion/ej2-navigations";
import {useSelector} from "react-redux";
import {selectSession} from "@/store/slices/projectSlice";
// import {srcFile} from "@/lib/userData";


DocumentEditorContainerComponent.Inject(Toolbar);

export default function Editor({userSession, headerTitle}: { userSession: Session | null, headerTitle: string }) {

    const session = useSelector(selectSession)
    const isInitialized = useRef(false);
    const contentChanged = useRef(false);
    const container = useRef<DocumentEditorContainerComponent>(null);
    const [docxHash, setDocxHash] = useState<string | null>(null)
    const [commentsHash, setCommentsHash] = useState<string | null>(null)


    useEffect(() => {
        if (!isInitialized.current) {
            renderComplete();
            isInitialized.current = true;
        }
    }, []);

    useEffect(() => {
        const intervalId = setInterval(() => {
            if (contentChanged.current) {
                //You can save the document as below
                container?.current!.documentEditor
                    .saveAsBlob("Docx")
                    .then(async (blob: Blob) => {
                        const comments = container?.current!.documentEditor.getComments().map(comment => {
                            return {
                                ...comment,
                                replies: JSON.parse(JSON.stringify(comment.replies))
                            }
                        })

                        const result = await handleEditorChanges(blob, comments, docxHash, commentsHash)
                        console.log(result)
                        if (result.success) {
                            if (result.docxHash) setDocxHash(result.docxHash)
                            if (result.commentsHash) setCommentsHash(result.commentsHash)
                        }

                        const span = document.createElement("span");
                        const date = new Date();
                        const time = date.getHours() +
                            ":" +
                            date.getMinutes() +
                            ":" +
                            date.getSeconds();
                        span.innerHTML = "Auto saved at <b>" + time + "</b><hr>";
                    });
                contentChanged.current = false;
            }
        }, 3000);

        return () => clearInterval(intervalId);
    }, []);

    const hostUrl: string = "https://services.syncfusion.com/react/production/api/documenteditor/";
    let titleBar: TitleBar;

    const onLoadDefault = async () => {
        const srcFileData = await srcFile();
        container.current!.documentEditor.currentUser = `${userSession?.userData?.first_name} ${userSession?.userData?.last_name}`
        if (srcFileData) {
            try {
                const fileData = srcFileData;
                const binaryContent = atob(fileData.content);
                const fileBlob = new Blob([Uint8Array.from(binaryContent.split('').map(char => char.charCodeAt(0)))], {type: fileData.type});

                if (fileData.type === 'application/pdf') {
                    // Handle PDF files
                    const pdfData = await fileBlob.arrayBuffer();
                    const pdfjsLib = await import('pdfjs-dist');
                    // Configure PDF.js worker
                    pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

                    const pdf = await pdfjsLib.getDocument({data: pdfData}).promise;
                    let textContent = '';

                    // Extract text from all pages
                    for (let i = 1; i <= pdf.numPages; i++) {
                        const page = await pdf.getPage(i);
                        const text = await page.getTextContent();
                        textContent += text.items
                            .map((item: any) => item.str)
                            .join(' ') + '\n';
                    }

                    // Convert to SFDT format
                    const sfdtContent = {
                        sections: [{
                            blocks: [{
                                inlines: [{
                                    text: textContent
                                }]
                            }]
                        }]
                    };

                    container.current!.documentEditor.open(JSON.stringify(sfdtContent));
                } else {
                    // Handle text and docx files
                    const reader = new FileReader();
                    reader.onload = (event) => {

                        if (fileData.type === 'text/plain') {
                            // Convert plain text to SFDT while preserving formatting
                            const text = event.target?.result as string;
                            const paragraphs = text.split('\n');

                            // Function to detect if text contains RTL script
                            const containsRTL = (text: string) => {
                                const rtlRegex = /[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]/;
                                return rtlRegex.test(text);
                            };
                            const isRTL = containsRTL(text);
                            console.log(isRTL)
                            const sfdtContent = {
                                sections: [{
                                    sectionFormat: {
                                        pageWidth: 612,
                                        pageHeight: 792,
                                        leftMargin: 72,
                                        rightMargin: 72,
                                        topMargin: 72,
                                        bottomMargin: 72,
                                        bidi: isRTL
                                    },
                                    blocks: paragraphs.map(paragraph => ({
                                        paragraphFormat: {
                                            afterSpacing: 6,
                                            lineSpacing: 1.15,
                                            bidi: isRTL,
                                            textAlignment: isRTL ? 'Right' : 'Left',
                                            rightIndent: 0,
                                            leftIndent: 0
                                        },
                                        inlines: [{
                                            text: paragraph,
                                            characterFormat: {
                                                fontSize: 11,
                                                fontFamily: isRTL ? 'Arial' : 'Calibri',
                                                bidi: isRTL
                                            }
                                        }]
                                    })).filter(block => block.inlines[0].text.trim() !== '')
                                }]
                            };

                            container.current!.documentEditor.open(JSON.stringify(sfdtContent));

                            // Set document direction after opening
                            if (isRTL) {
                                setTimeout(() => {
                                    container.current!.documentEditor.selection.selectAll();
                                    container.current!.documentEditor.selection.paragraphFormat.textAlignment = 'Right';
                                    container.current!.documentEditor.selection.characterFormat.bidi = true;
                                    container.current!.documentEditor.selection.paragraphFormat.bidi = true;
                                    container.current!.documentEditor.selection.sectionFormat.bidi = true;
                                    container.current!.documentEditor.selection.moveToLineStart();
                                }, 20);
                            }
                        } else {
                            // For docx files, use direct content
                            container.current!.documentEditor.open(event.target?.result as string);
                        }
                    };

                    if (fileData.type === 'text/plain') {
                        reader.readAsText(fileBlob);
                    } else {
                        reader.readAsBinaryString(fileBlob);
                    }
                }
            } catch (error) {
                console.error('Error loading file:', error);
                container.current!.documentEditor.open(JSON.stringify(data));
            }
        } else {
            container.current!.documentEditor.open(JSON.stringify(data));
        }

        container.current!.documentEditor.documentName = headerTitle;
        container.current!.documentEditorSettings.showRuler = true;
        titleBar.updateDocumentTitle()
        container.current!.documentChange = () => {
            titleBar.updateDocumentTitle();
            container.current!.documentEditor.focusIn();
        };
        const menuItems: MenuItemModel[] = [
            {
                text: 'Search In Google',
                id: 'search_in_google',
                iconCss: 'e-icons e-de-ctnr-find',
            },
            {
                text: `Copy to 'Side by side'`,
                id: 'search_in_google',
                iconCss: 'e-icons e-undo',
            },
        ];
        // adding Custom Options
        container.current.documentEditor.contextMenu.addCustomMenu(menuItems, false);

        container.current.documentEditor.customContextMenuSelect = (args: any): void => {
            // custom Options Functionality
            const id: string = container.current.documentEditor.element.id;
            switch (args.id) {
                case id + 'search_in_google':
                    // To get the selected content as plain text
                    const searchContent: string =
                        container.current.documentEditor.selection.text;
                    if (
                        !container.current.documentEditor.selection.isEmpty &&
                        /\S/.test(searchContent)
                    ) {
                        window.open('http://google.com/search?q=' + searchContent);
                    }
                    break;
            }
        };
    }
    const renderComplete = () => {
        window.onbeforeunload = function () {
            return "Want to save your changes?";
        };
        container.current!.documentEditor.pageOutline = "#E0E0E0";
        container.current!.documentEditor.acceptTab = true;
        container.current!.documentEditor.resize();
        titleBar = new TitleBar(document.getElementById(`documenteditor_titlebar`), container.current!.documentEditor, true);
        onLoadDefault();


        container.current!.contentChange = () => {
            contentChanged.current = true;
        };

    };

    return (
        <div id={`documenteditor_container_body`}>
            <div className="control-pane">
                <div className="control-section">
                    <div id={`documenteditor_titlebar`}
                         className="e-de-ctn-title"></div>
                    <DocumentEditorContainerComponent id={`container`} ref={container}
                                                      className="transition-all duration-300 ease-in-out block"
                                                      serviceUrl={hostUrl}
                                                      zIndex={3000}
                                                      enableToolbar={true}
                                                      height={"780px"}
                                                      showPropertiesPane={true}
                                                      enableTrackChanges={true}
                                                      layoutType={"Pages"}
                                                      locale="en-US"/>
                </div>
            </div>
        </div>
    )
};
