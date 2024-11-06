'use client'

import { DocumentEditorContainerComponent } from '@syncfusion/ej2-react-documenteditor';
import { EditorProps } from './types';

export default function DocumentContainer({ 
    container, 
    hostUrl,
    isView
}: EditorProps) {
    return (
        <DocumentEditorContainerComponent 
            id={`container`} 
            ref={container}
            className="transition-all duration-300 ease-in-out block"
            serviceUrl={hostUrl}
            zIndex={3000}
            enableToolbar={true}
            height={"780px"}
            showPropertiesPane={!isView}
            enableTrackChanges={true}
            layoutType={"Pages"}
            locale="en-US"
        />
    );
}
