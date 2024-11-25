export interface PriorityProps {
    [key: string]: number;
}

export interface ILanguages {
    [key: string]: string;
}

export interface IStatus {
    [key: string]: string;
}

export interface StatusObject {
    label: string;
    color: string;
    value: string;
}

export interface PriorityObject {
    label: string;
    color: string;
    value: number;
}