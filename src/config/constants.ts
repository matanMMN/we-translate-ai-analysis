import {ILanguages, IStatus, PriorityObject, PriorityProps, StatusObject} from "@/config/constants.interface";


export const AppName: string = "WeTranslate AI"

export const Status: IStatus = {
    PENDING: "pending",
    ON_HOLD: "on hold",
    COMPLETE: "complete"
}

export const statusesArray: Array<StatusObject> = [
    {label: 'Pending', color: 'black', value: Status.PENDING},
    {label: 'On Hold', color: 'gray', value: Status.ON_HOLD},
    {label: 'Complete', color: 'lightgreen', value: Status.COMPLETE}
];


export const Priority: PriorityProps = {
    TOP: 5,
    HIGH: 4,
    NORMAL: 3,
    LOW: 2,
    LOWEST: 1
}
export const prioritiesArray: Array<PriorityObject> = [
    {label: 'Top', color: 'red', value: Priority.TOP},
    {label: 'High', color: 'orange', value: Priority.HIGH},
    {label: 'Normal', color: 'blue', value: Priority.NORMAL},
    {label: 'Low', color: 'lightgreen', value: Priority.LOW},
    {label: 'Lowest', color: 'gray', value: Priority.LOWEST}
];


export const languages: ILanguages = {
    ENGLISH: "English",
    HEBREW: "Hebrew",
    ARABIC: "Arabic"
}


export const supportedSourceLanguages = ['en', 'he'] as const
export const supportedTargetLanguages = ['en', 'he', 'ar'] as const
export const statuses: Array<string> = Object.values(Status);
export const priorities: Array<number> = Object.values(Priority);