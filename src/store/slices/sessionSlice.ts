import {createSlice, PayloadAction} from '@reduxjs/toolkit';
import {RootState} from '../store.types';
import {Project} from '@/lib/userData';
import {Session} from 'next-auth';

export interface ProjectState {
    projectId: string | null;
    project: Project | null;
    userSession: Session | null;
}

const initialState: ProjectState = {
    projectId: null,
    project: null,
    userSession: null,
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
    },
});

export const {setSessionSlice} = sessionSlice.actions;
export const selectSession = (state: RootState) => state.session;
export default sessionSlice.reducer;