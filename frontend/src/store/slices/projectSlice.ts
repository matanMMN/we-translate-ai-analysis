import {createSlice, PayloadAction} from '@reduxjs/toolkit'

interface ProjectFiles {
    srcFileId: string | null
    targetFileId: string | null
    refFileId: string | null
}

interface FileMetadata {
    blob?: Blob | null | undefined,
    type?: string | null | undefined,
    docxHash?: string | null
    commentsHash?: string | null
    lastModified?: number | null
}

interface ProjectState {
    id: string | null
    files: ProjectFiles
    currentFile: FileMetadata
    loading: boolean
    error: string | null
}

const initialState: ProjectState = {
    id: null,
    files: {
        srcFileId: null,
        targetFileId: null,
        refFileId: null
    },
    currentFile: {
        blob: null,
        type: null,
        docxHash: null,
        commentsHash: null,
        lastModified: null
    },
    loading: false,
    error: null
}

export const projectSlice = createSlice({
    name: 'project',
    initialState,
    reducers: {
        initializeProject: (state, action: PayloadAction<{
            id: string,
            files?: ProjectFiles
        }>) => {
            state.id = action.payload.id
            if (action.payload.files) {
                state.files = action.payload.files
            }
        },

        updateFileMetadata: (state, action: PayloadAction<FileMetadata>) => {
            state.currentFile = {
                ...state.currentFile,
                ...action.payload,
                lastModified: Date.now()
            }
        },

        setTranslatedFile: (state, action: PayloadAction<{
            fileId?: string,
            blob: Blob,
            type: string, //txt, pdf, docx
            // docxHash?: string,
            // commentsHash?: string | null
        }>) => {
            console.log("set")
            // state.files.srcFileId = action.payload.fileId
            state.currentFile.blob = action.payload.blob
            state.currentFile.type = action.payload.type
            state.currentFile.lastModified = Date.now()
            // state.currentFile = {
            //     docxHash: action.payload.docxHash,
            //     commentsHash: action.payload.commentsHash,
            //     lastModified: Date.now()
            // }
        },

        setCurrentFileMetadata: (state, action: PayloadAction<FileMetadata>) => {
            state.currentFile = action.payload
        },

        setLoading: (state, action: PayloadAction<boolean>) => {
            state.loading = action.payload
        },

        setError: (state, action: PayloadAction<string | null>) => {
            state.error = action.payload
        }
    }
})

// Actions
export const {
    initializeProject,
    updateFileMetadata,
    setTranslatedFile,
    setCurrentFileMetadata,
    setLoading,
    setError
} = projectSlice.actions

// Selectors
export const selectProjectId = (state: { project: ProjectState }) => state.project.id
export const selectProjectFiles = (state: { project: ProjectState }) => state.project.files
export const selectCurrentFile = (state: { project: ProjectState }) => state.project.currentFile
export const selectSrcFileId = (state: { project: ProjectState }) => state.project.files.srcFileId

export default projectSlice.reducer