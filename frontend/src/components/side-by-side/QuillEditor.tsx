'use client'

import {useEffect, useState, useRef, RefObject} from 'react';
import dynamic from 'next/dynamic';
import {useAppDispatch} from '@/hooks/useAppDispatch';
import {updateSection, syncWithBackend, selectSections} from '@/store/slices/sideBySideSlice';
import 'react-quill-new/dist/quill.snow.css';
import type ReactQuill from 'react-quill-new';
import {debounce} from 'lodash';
import {useAppSelector} from "@/hooks/useAppSelector";

// Add proper types for the dynamic import component
type QuillProps = {
    forwardedRef: React.RefObject<ReactQuill>;
    [key: string]: string | number | RefObject<ReactQuill> | string[] | ((value: string) => void) | boolean | undefined | ModuleProps;
};

const ReactQuillComponent = dynamic(
    async () => {
        const {default: RQ} = await import('react-quill-new');
        return function comp({forwardedRef, ...props}: QuillProps) {
            return <RQ ref={forwardedRef} {...props} />;
        };
    },
    {
        ssr: false,
        loading: () => <div className="h-full animate-pulse bg-gray-100 rounded-md"/>
    }
);

interface QuillEditorProps {
    id: string;
    content: string;
    readOnly?: boolean;
    isRTL?: boolean;
    projectId?: string;
}

interface ModuleProps {
    toolbar: Array<Array<string | object>>;
}

const modules: ModuleProps = {
    toolbar: [
        [{'header': '1'}, {'header': '2'}, {'font': ['Arial']}],
        [{'size': ['Normal']}],
        ['bold', 'italic', 'underline', 'strike', 'blockquote'],
        [{'list': 'ordered'}, {'list': 'bullet'}, {'indent': '-1'}, {'indent': '+1'}],
        [{'script': 'sub'}, {'script': 'super'}],
        [{'align': ''}, {'align': 'center'}, {'align': 'right'}, {'align': 'justify'}],
        ['clean']
    ]
};

const formats = [
    'header', 'font', 'size',
    'bold', 'italic', 'underline', 'strike', 'blockquote',
    'list', 'indent',
    'script',
    'align', 'direction'
];

export function QuillEditor({id, content, readOnly = false, isRTL = false, projectId}: QuillEditorProps) {

    const editor = useRef<ReactQuill>(null);
    const dispatch = useAppDispatch();
    const sections = useAppSelector(selectSections);
    const [mounted, setMounted] = useState(false);
    // Create debounced sync function
    const debouncedSync = useRef(
        debounce((sections, projectId) => {
            dispatch(syncWithBackend({projectId, sections}));
        }, 1000)
    ).current;

    useEffect(() => {
        debouncedSync(sections, projectId);
    }, [debouncedSync, projectId, sections])

    useEffect(() => {
        setMounted(true);
    }, []);

    const handleChange = (value: string) => {
        dispatch(updateSection({
            id,
            [readOnly ? 'sourceContent' : 'targetContent']: value,
            projectId
        }));

        // Trigger sync with backend
        // if (projectId) {
        //     if (readOnly)
        //         debouncedSync(sections.map(s => s.id === id ?), projectId);
        //     else
        //         debouncedSync(sections.map(s => s.id === id ?), projectId);
        // }
    };

    if (!mounted) {
        return <div className="h-full animate-pulse bg-gray-100 rounded-md"/>;
    }

    return (
        <div className={`quill-container ${isRTL ? 'rtl' : 'ltr'} h-[calc(100vh-500px)]`}>
            <ReactQuillComponent
                forwardedRef={editor}
                id={id + (readOnly ? '-source' : '-target')}
                theme="snow"
                value={content}
                defaultValue={"Waiting for data"}
                onChange={handleChange}
                tabIndex={1}
                bounds={'#quills'}
                modules={modules}
                formats={formats}
                readOnly={readOnly || !content}
                placeholder={readOnly ? "Source text will appear here..." : "Translated text will appear here..."}
                className={`h-[calc(100%-42px)] max-h-[calc(100vh-300px)] ${isRTL ? 'text-right' : 'text-left'}`}
                preserveWhitespace={false}
            />
        </div>
    );
}
