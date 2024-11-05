import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { useDispatch, useSelector } from "react-redux";
import { selectSourceLanguage, selectTargetLanguage, setSourceLanguage } from "@/store/slices/sideBySideSlice";

export function LanguageSelector() {
    const dispatch = useDispatch();
    const sourceLanguage = useSelector(selectSourceLanguage);
    const targetLanguage = useSelector(selectTargetLanguage);

    return (
        <div className="grid grid-cols-2 gap-4 mb-4">
            <Select value={sourceLanguage} onValueChange={(value) => dispatch(setSourceLanguage(value))}>
                <SelectTrigger className="bg-gray-50">
                    <SelectValue placeholder="Select language" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="en">English</SelectItem>
                    <SelectItem value="he">Hebrew</SelectItem>
                </SelectContent>
            </Select>
            <div className="bg-gray-50 rounded-md px-4 py-2 flex items-center justify-between">
                {targetLanguage}
            </div>
        </div>
    );
} 