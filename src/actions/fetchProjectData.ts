'use server'

import store from '@/store/store'
import {setCurrentFileMetadata} from '@/store/slices/projectSlice'

interface ProjectDataResponse {
    docxHash: null,
    commentsHash: null,
    lastModified: null
}

export async function fetchProjectData(projectId: string): Promise<ProjectDataResponse | null> {
    try {
        // In development, read from local file system
        // if (process.env.NODE_ENV === 'development') {
            console.log(projectId)
            store.dispatch(setCurrentFileMetadata({
                docxHash: null,
                commentsHash: null,
                lastModified: Date.parse("2024-10-31")
            }))
            return null;
        // }

        // // TODO: In production, fetch from actual storage using projectId
        // return null
    } catch (error) {
        console.error('Error fetching project file:', error)
        return null
    }
}