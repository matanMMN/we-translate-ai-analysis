import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface ProjectState {
    projectId: string | null;
    userSession: any | null;
    project: any | null;
}

const initialState: ProjectState = {
    projectId: null,
    userSession: null,
    project: null,
};

const projectSlice = createSlice({
    name: 'project',
    initialState,
    reducers: {
        setSessionSlice: (state, action: PayloadAction<ProjectState>) => {
            return action.payload;
        },
        setProjectId: (state, action: PayloadAction<string>) => {
            state.projectId = action.payload;
        },
        setUserSession: (state, action: PayloadAction<any>) => {
            state.userSession = action.payload;
        },
        setProject: (state, action: PayloadAction<any>) => {
            state.project = action.payload;
        },
    },
});

export const selectSession = (state: { project: ProjectState }) => state.project;
export const selectProjectId = (state: { project: ProjectState }) => state.project.projectId;
export const selectUserSession = (state: { project: ProjectState }) => state.project.userSession;
export const selectProject = (state: { project: ProjectState }) => state.project.project;
export const { setProjectId, setUserSession, setProject, setSessionSlice } = projectSlice.actions;
export default projectSlice.reducer;