import {createSlice, PayloadAction} from '@reduxjs/toolkit';
import {RootState} from '../store.types';
import {Project} from '@/lib/userData';
import {createAsyncThunk} from '@reduxjs/toolkit';

export const clearAllLocalStorage = createAsyncThunk(
    'localStorage/clearAll',
    async ({projectId}: { projectId: string }) => {
        localStorage.setItem(`sideBySideSections_${projectId}`, JSON.stringify({}));
    }
);

export interface CachedProject {
    data: Project;
    timestamp: number;
}

export interface ProjectCache {
    [key: string]: CachedProject;
}

export interface ProjectCacheState {
    cache: ProjectCache;
    expiryTime: number;
    lastRevalidation: number | null;
}

const initialState: ProjectCacheState = {
    cache: {},
    expiryTime: 5 * 60 * 1000, // 5 minutes
    lastRevalidation: null,
};

const projectCacheSlice = createSlice({
    name: 'projectCache',
    initialState,
    reducers: {
        cacheProject: (
            state,
            action: PayloadAction<{ projectId: string; project: Project }>
        ) => {
            state.cache[action.payload.projectId] = {
                data: action.payload.project,
                timestamp: Date.now(),
            };
        },
        clearCache: (state) => {
            state.cache = {};
            state.lastRevalidation = null;
        },
        removeFromCache: (state, action: PayloadAction<string>) => {
            delete state.cache[action.payload];
        },
        updateCacheEntry: (
            state,
            action: PayloadAction<{ projectId: string; project: Project }>
        ) => {
            if (state.cache[action.payload.projectId]) {
                state.cache[action.payload.projectId] = {
                    data: action.payload.project,
                    timestamp: Date.now(),
                };
            }
        },
        setLastRevalidation: (state) => {
            state.lastRevalidation = Date.now();
        },
    },
});


export const selectProjectFromCache = (projectId: string) =>
    (state: RootState) => state.projectCache.cache[projectId];

export const selectCacheExpiryTime = (state: RootState) =>
    state.projectCache.expiryTime;

export const selectLastRevalidation = (state: RootState) =>
    state.projectCache.lastRevalidation;

export const {
    cacheProject,
    clearCache,
    removeFromCache,
    updateCacheEntry,
    setLastRevalidation,
} = projectCacheSlice.actions;

export default projectCacheSlice.reducer; 