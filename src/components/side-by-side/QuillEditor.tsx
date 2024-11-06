'use client'

import {useEffect, useState, useRef} from 'react';
import dynamic from 'next/dynamic';
import {useAppDispatch} from '@/hooks/useAppDispatch';
import {updateSection} from '@/store/slices/sideBySideSlice';
import 'react-quill-new/dist/quill.snow.css';

// Dynamic import with specific settings to avoid SSR issues
const ReactQuill = dynamic(
    async () => {
        const {default: RQ} = await import('react-quill-new');
        // @ts-ignore
        return function comp({forwardedRef, ...props}) {
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
}

const modules = {
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

export function QuillEditor({id, content, readOnly = false, isRTL = false}: QuillEditorProps) {

    const editor = useRef(null)
    const dispatch = useAppDispatch();
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    const handleChange = (value: string) => {
        dispatch(updateSection({
            id,
            [readOnly ? 'sourceContent' : 'targetContent']: value
        }));
    };

    if (!mounted) {
        return <div className="h-full animate-pulse bg-gray-100 rounded-md"/>;
    }

    // Add wrapper div for RTL support
    return (
        <div className={`${isRTL ? 'text-right' : 'text-left'} flex max-h-[calc(100vh-500px)]`}>
            <div className={`${isRTL ? 'ql-rtl' : 'ql-ltr'}`}>
                <ReactQuill
                    ref={editor}
                    id={id + (readOnly ? '-source' : '-target')}
                    theme="snow"
                    value={content}
                    defaultValue={"Waiting for data"}
                    onChange={handleChange}
                    tabIndex={1}
                    bounds={'#quills'}
                    modules={modules}
                    formats={formats}
                    style={{flex: "1", textAlign: `${isRTL ? 'right' : 'left'}`}}
                    readOnly={readOnly || !content}
                    // onChangeSelection={}
                    // onFocus={}
                    // onBlur={}
                    placeholder={readOnly ? "Source text will appear here..." : "Translate text will appear here..."}
                    className="h-[calc(100%-42px)] max-h-[calc(100vh-300px)]"
                    preserveWhitespace={false}
                />
            </div>
        </div>
    );
}
