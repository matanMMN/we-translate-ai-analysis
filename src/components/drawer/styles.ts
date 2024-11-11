import {StyleProps} from "./types";

export const getButtonStyles = ({isActive}: StyleProps) => {
    const baseStyles = [
        "w-full",
        "justify-center",
        "items-center",
        "text-start",
        "hover:border-none",
        "border-none",
        "border-b-4",
        "rounded-md",
        "inline-flex",
        "px-2",
        "py-1",
        "pl-2",
        "ring-transparent",
        "ring-0",
        "m-0",
        "gap-0",
        "my-2",
        "border",
        "rounded-2xl",
        "transition-colors",
    ].join(" ");


    return `${baseStyles} ${isActive ? 'bg-primary' : 'bg-transparent hover:bg-gray-200'}`;
};

export const getIconStyles = ({isActive, isLogout = false}: StyleProps) => {
    const baseStyles = "gap-0 m-0 p-0 transition-colors";

    if (isLogout) {
        return `${baseStyles} text-black`;
    }

    return `${baseStyles} ${
        isActive ? 'text-white' : 'text-black'
    }`;
};

export const getTextStyles = ({isActive, isLogout = false}: StyleProps) => {
    const baseStyles = "text-2xl transition-colors";

    if (isLogout) {
        return `${baseStyles} text-black`;
    }

    return `${baseStyles} ${isActive ? 'text-white' : 'text-black'}`;
};