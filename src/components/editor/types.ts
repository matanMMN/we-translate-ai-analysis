import {DocumentEditorContainerComponent} from '@syncfusion/ej2-react-documenteditor';
import {RefObject} from 'react';
import {Dialog} from "@syncfusion/ej2-popups";

export interface EditorProps {
    container: RefObject<DocumentEditorContainerComponent>;
    hostUrl: string;
    isView?: boolean
}

export interface EditorConfig {
    readOnly?: boolean;
    closeButton?: boolean,
    projectId?: string;
    dialogRef?: RefObject<Dialog>
}

export interface FileData {
    content: string;
    type: string;
    name: string;
} 