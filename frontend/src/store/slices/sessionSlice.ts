import {createSlice, PayloadAction} from '@reduxjs/toolkit';
import {RootState} from '../store.types';
import {Project} from '@/lib/userData';
import {Session} from 'next-auth';

export interface ProjectState {
    projectId: string | null;
    project: Project | null;
    userSession: Session | null;
    curPath?: string;
}

const initialState: ProjectState = {
    projectId: null,
    project: null,
    userSession: null,
    curPath: ''
};

const sessionSlice = createSlice({
    name: 'session',
    initialState,
    reducers: {
        setSessionSlice: (state, action: PayloadAction<ProjectState>) => {
            state.projectId = action.payload.projectId;
            state.project = action.payload.project;
            state.userSession = action.payload.userSession;
        },
        setPath: (state, action: PayloadAction<string>) => {
            state.curPath = action.payload;
        },
        setProjectTargetFileId: (state, action: PayloadAction<string | undefined>) => {
            if (state.project && action.payload) {
                state.project.target_file_id = action.payload;
            }
        }
    },
});

export const {setSessionSlice, setPath, setProjectTargetFileId} = sessionSlice.actions;
export const selectSession = (state: RootState) => state.session;
export const selectPath = (state: RootState) => state.session.curPath;
export default sessionSlice.reducer;