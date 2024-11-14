import {Project} from "@/lib/userData";


export const getStatus = (status: string) => {
    switch (status) {
        case 'initial':
            return 'In Progress'
        // case 'Planned':
        //     return 'text-slate-500'
        // case 'In Progress':
        //     return 'text-blue-500'
        // case 'Completed':
        //     return 'text-emerald-500'
        // case 'On Hold':
    }

}

export const getLanguage = (language: string) => {
    switch (language) {
        case 'en':
        case 'english':
        case 'English':
            return 'English'
        case 'he':
        case 'hebrew':
        case 'Hebrew':
            return 'Hebrew'
        case 'ar':
        case 'arabic':
        case 'Arabic':
            return 'Arabic'
        case 'fr':
        case 'french':
        case 'French':
            return 'French'
        case 'de':
        case 'german':
        case 'German':
            return 'German'
        case 'es':
        case 'spanish':
        case 'Spanish':
            return 'Spanish'
        case 'it':
        case 'italian':
        case 'Italian':
            return 'Italian'
        default:
            return 'Unknown'
    }
}

export const getPriority = (priority: string | number) => {
    switch (priority) {
        case 0:
            return 'Low'
        case 1:
            return 'Normal'
        case 2:
            return 'High'
        case 3:
            return 'Critical'
    }
}

export const getPriorityColor = (priority: Project['priority']) => {
    switch (priority) {
        case 'Low':
        case 0 :
            return 'bg-emerald-500/10 text-emerald-500'
        case 'Normal':
        case 1:
            return 'bg-blue-500/10 text-blue-500'
        case 'High':
        case 2:
            return 'bg-amber-500/10 text-amber-500'
        case 'Critical':
        case 3:
            return 'bg-red-500/10 text-red-500'
    }
}

export const getStatusColor = (status: Project['status']) => {
    console.log(status)
    return 'text-slate-500'
    // switch (status) {
    //     case 'Planned':
    //         return 'text-slate-500'
    //     case 'In Progress':
    //         return 'text-blue-500'
    //     case 'Completed':
    //         return 'text-emerald-500'
    //     case 'On Hold':
    //         return 'text-amber-500'
    // }
}
