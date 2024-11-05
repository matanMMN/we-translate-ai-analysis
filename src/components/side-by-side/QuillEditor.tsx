'use client'

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { useAppDispatch } from '@/hooks/useAppDispatch';
import { updateSection } from '@/store/slices/sideBySideSlice';
import 'react-quill/dist/quill.snow.css';

const ReactQuill = dynamic(() => import('react-quill'), {
    ssr: false,
    loading: () => <div className="h-full animate-pulse bg-gray-100 rounded-md" />
});

interface QuillEditorProps {
    id: string;
    content: string;
    readOnly?: boolean;
    isRTL?: boolean;
}

const modules = {
    toolbar: [
        [{ 'font': ['Arial'] }],
        [{ 'size': ['Normal'] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ 'script': 'sub'}, { 'script': 'super' }],
        [{ 'align': [] }],
        ['clean']
    ]
};

const formats = [
    'font',
    'size',
    'bold',
    'italic',
    'underline',
    'strike',
    'script',
    'align'
];

export function QuillEditor({ id, content, readOnly = false, isRTL = false }: QuillEditorProps) {
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
        return <div className="h-full animate-pulse bg-gray-100 rounded-md" />;
    }

    return (
        <div className={`h-full ${isRTL ? 'text-right' : 'text-left'}`}>
            <ReactQuill
                theme="snow"
                value={content}
                onChange={handleChange}
                modules={modules}
                formats={formats}
                readOnly={readOnly}
                placeholder={readOnly ? "Source text will appear here..." : "Enter translation..."}
                className={`h-[calc(100%-42px)] ${isRTL ? 'ql-rtl' : 'ql-ltr'}`}
            />
        </div>
    );
} 