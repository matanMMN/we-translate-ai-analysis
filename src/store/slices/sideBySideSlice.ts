import {createSlice, PayloadAction, createAsyncThunk} from '@reduxjs/toolkit';
import {RootState} from '../store.types';
import {v4 as uuid} from 'uuid';
import {compareAsc} from 'date-fns';
import {getUser} from "@/lib/AuthGuard";
import {serverUrl} from "@/lib/functions";

interface Section {
    id: string;
    sourceContent: string;
    targetContent: string;
    lastModified?: string;
    projectId?: string | undefined
    sourceLanguage: string;
    targetLanguage: string
}

interface SideBySideState {
    sections: Section[];
    projectId: string;
    activeSection: string;
    isLoading: boolean;
    error: string | null;
}

const initialState: SideBySideState = {
    sections: [],
    projectId: '',
    activeSection: '1',
    isLoading: false,
    error: null
};

export const deleteSectionAndSync = createAsyncThunk(
    'sideBySide/deleteSectionAndSync',
    async ({id, projectId}: { id: string, projectId: string }, {dispatch, getState}) => {
        dispatch(deleteSection({id, projectId}));
        const state = getState() as RootState;
        const sections = selectSections(state);
        await dispatch(syncWithBackend({projectId, sections}));
    }
);

// new thunks for backend operations
export const syncWithBackend = createAsyncThunk(
    'sideBySide/syncWithBackend',
    async ({projectId, sections}: {
        projectId: string,
        sections: Section[]
    }, {rejectWithValue}) => {
        try {

            const user = await getUser()

            if (!user) {
                return rejectWithValue('User authentication failed')
            }
            const authToken = user.accessToken
            const response = await fetch(`${serverUrl}/jobs/${projectId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authToken}`
                },
                body: JSON.stringify({
                    data: {
                        sideBySideSections: sections.map(section => ({
                            ...section,
                            lastModified: section.lastModified || new Date().toISOString()
                        }))
                    }
                })
            });

            if (!response.ok) throw new Error('Failed to sync with backend');
            return await response.json();
        } catch (error) {
            return rejectWithValue((error as Error).message);
        }
    }
);

export const fetchSectionsData = createAsyncThunk(
    'sideBySide/fetchSectionsData',
    async ({projectId}: { projectId: string }, {rejectWithValue}) => {
        try {
            const user = await getUser()
            if (!user) {
                return rejectWithValue('User authentication failed')
            }
            const authToken = user.accessToken

            // Get data from localStorage
            const localData = localStorage.getItem(`sideBySideSections_${projectId}`);
            const localSections = localData ? JSON.parse(localData) : null;
            const localLastModified = localSections?.lastModified || '1970-01-01';

            // Get data from backend
            const response = await fetch(`${serverUrl}/jobs/${projectId}`, {headers: {'Authorization': `Bearer ${authToken}`}});
            if (!response.ok) throw new Error('Failed to fetch from backend');
            const backendData = await response.json();
            const backendSections = backendData.data?.data?.sideBySideSections || [];
            const backendLastModified = backendSections.length > 0
                ? Math.max(...backendSections.map((s: Section) => new Date(s.lastModified || '1970-01-01').getTime()))
                : '1970-01-01';

            // Compare dates and return the newest data
            if (compareAsc(new Date(localLastModified), new Date(backendLastModified)) > 0) {
                return localSections.sections;
            }
            return backendSections;
        } catch (error) {
            return rejectWithValue((error as Error).message);
        }
    }
);

const sideBySideSlice = createSlice({
    name: 'sideBySide',
    initialState,
    reducers: {
        updateSection: (state, action: PayloadAction<{
            id: string;
            sourceContent?: string;
            targetContent?: string;
            projectId?: string
        }>) => {
            const section = state.sections.find(s => s.id === action.payload.id);
            if (section) {
                if (action.payload.sourceContent !== undefined) {
                    section.sourceContent = action.payload.sourceContent;
                }
                if (action.payload.targetContent !== undefined) {
                    section.targetContent = action.payload.targetContent;
                }
                section.lastModified = new Date().toISOString();

                // Update localStorage
                localStorage.setItem(`sideBySideSections_${action.payload.projectId}`, JSON.stringify({
                    sections: state.sections,
                    lastModified: new Date().toISOString()
                }));
            }
        },
        setActiveSection: (state, action: PayloadAction<string>) => {
            state.activeSection = action.payload;
        },
        setTargetLanguage: (state, action: PayloadAction<string>) => {
            if (state.activeSection && !!state.sections.length) {
                const targetSection = state.sections.find((section: Section) => section!.id! === state!.activeSection!)
                targetSection!.targetLanguage = action.payload;
            }
        },
        initializeWithText: (state, action: PayloadAction<{
            text: string;
            sourceLanguage?: string;
            projectId?: string
        }>) => {
            const newSection: Section = {
                id: uuid(),
                sourceContent: action.payload.text,
                targetContent: '',
                lastModified: new Date().toISOString(),
                sourceLanguage: action.payload.sourceLanguage || "en",
                targetLanguage: 'he',
                projectId: action.payload.projectId!,
            };
            state.sections.push(newSection);
            state.projectId = action.payload.projectId!
            state.activeSection = newSection.id;

            localStorage.setItem(`sideBySideSections_${state.projectId}`, JSON.stringify({
                sections: state.sections,
                lastModified: new Date().toISOString()
            }));

        },
        deleteSection: (state, action: PayloadAction<string | { id: string, projectId: string }>) => {
            const sectionId = typeof action.payload === 'string' ? action.payload : action.payload.id;
            state.sections = state.sections.filter(s => s.id !== sectionId);
            if (state.activeSection === sectionId) {
                state.activeSection = state.sections[0]?.id || '1';
            }

            // Update localStorage
            localStorage.setItem(`sideBySideSections_${state.projectId || (typeof action.payload !== 'string' && action.payload.projectId)}`, JSON.stringify({
                sections: state.sections,
                lastModified: new Date().toISOString()
            }));

        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchSectionsData.fulfilled, (state, action) => {
                state.sections = action.payload;
                state.activeSection = action.payload[0]?.id || '1';
                state.isLoading = false;
            })
            .addCase(syncWithBackend.fulfilled, (state) => {
                state.isLoading = false;
            })
            .addCase(deleteSectionAndSync.pending, (state) => {
                state.isLoading = true;
            })
            .addCase(deleteSectionAndSync.fulfilled, (state) => {
                state.isLoading = false;
            })
            .addCase(deleteSectionAndSync.rejected, (state) => {
                state.isLoading = false;
            });
    }
});

// Actions
export const {
    updateSection,
    setActiveSection,
    setTargetLanguage,
    initializeWithText,
    deleteSection
} = sideBySideSlice.actions;

// Selectors
export const selectSections = (state: RootState) => state.sideBySide.sections;
export const selectActiveSection = (state: RootState) => state.sideBySide.activeSection;
export const selectSourceLanguage = (state: RootState) => state.sideBySide.sections.find((section) => section.id == state.sideBySide.activeSection)?.sourceLanguage;
export const selectTargetLanguage = (state: RootState) => state.sideBySide.sections.find((section) => section.id == state.sideBySide.activeSection)?.targetLanguage;
export const selectActiveSectionData = (state: RootState) =>
    state.sideBySide.sections.find((section: Section) => {
        return section.id == state.sideBySide.activeSection
    });
export const selectIsLoading = (state: RootState) => state.sideBySide.isLoading;
export const selectError = (state: RootState) => state.sideBySide.error;

export default sideBySideSlice.reducer;