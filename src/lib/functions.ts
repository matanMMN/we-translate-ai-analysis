import {Project} from "@/lib/userData";

export const getPriorityColor = (priority: Project['priority']) => {
    switch (priority) {
        case 'Low':
            return 'bg-emerald-500/10 text-emerald-500'
        case 'Normal':
            return 'bg-blue-500/10 text-blue-500'
        case 'High':
            return 'bg-amber-500/10 text-amber-500'
        case 'Critical':
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
