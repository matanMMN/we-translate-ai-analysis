import { useDispatch } from "react-redux";
import { updateSection } from "@/store/slices/sideBySideSlice";

interface TextEditorProps {
    id: string;
    content: string;
    readOnly?: boolean;
    placeholder?: string;
}

export function TextEditor({ id, content, readOnly = false, placeholder }: TextEditorProps) {
    const dispatch = useDispatch();

    const handleChange = (value: string) => {
        dispatch(updateSection({
            id,
            [readOnly ? 'targetContent' : 'sourceContent']: value
        }));
    };

    return (
        <div className="flex-1 bg-white rounded-b-md border">
            <textarea
                className="w-full h-full resize-none border-0 focus:outline-none bg-transparent p-4"
                placeholder={placeholder}
                value={content}
                onChange={(e) => handleChange(e.target.value)}
                readOnly={readOnly}
            />
        </div>
    );
} 