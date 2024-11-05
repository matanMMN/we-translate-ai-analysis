import {DocumentEditorContainerComponent} from '@syncfusion/ej2-react-documenteditor';
import {RefObject} from 'react';
import {Session} from 'next-auth';

export interface EditorProps {
    container: RefObject<DocumentEditorContainerComponent>;
    hostUrl: string;
}

export interface EditorConfig {
    userSession: Session | null;
    headerTitle: string;
    readOnly?: boolean;
    closeButton?: boolean,
    projectId?: string;
}

export interface FileData {
    content: string;
    type: string;
    name: string;
} 