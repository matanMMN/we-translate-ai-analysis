import { createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import { RootState } from '../store.types';

interface Section {
    id: string;
    sourceContent: string;
    targetContent: string;
    filePath?: string;  // Path to stored file
    lastModified?: string;
}

interface SideBySideState {
    sections: Section[];
    sourceLanguage: string | null;
    targetLanguage: string;
    activeSection: string;
    isLoading: boolean;
    error: string | null;
}

const initialState: SideBySideState = {
    sections: [],
    sourceLanguage: null,
    targetLanguage: 'he',
    activeSection: '1',
    isLoading: false,
    error: null
};

// Async thunks for file operations
export const saveSectionToFile = createAsyncThunk(
    'sideBySide/saveSection',
    async (section: Section, { rejectWithValue }) => {
        try {
            // First save to public/uploads
            const formData = new FormData();
            formData.append('sourceContent', section.sourceContent);
            formData.append('targetContent', section.targetContent);
            formData.append('sectionId', section.id);

            const response = await fetch('/api/sections/save', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Failed to save section');

            const data = await response.json();
            return data; // Returns { id, filePath, lastModified }
        } catch (error) {
            return rejectWithValue((error as Error).message);
        }
    }
);

export const fetchUserSections = createAsyncThunk(
    'sideBySide/fetchSections',
    async (_, { rejectWithValue }) => {
        try {
            const response = await fetch('/api/sections');
            if (!response.ok) throw new Error('Failed to fetch sections');
            return await response.json();
        } catch (error) {
            return rejectWithValue((error as Error).message);
        }
    }
);

const sideBySideSlice = createSlice({
    name: 'sideBySide',
    initialState,
    reducers: {
        addSection: (state) => {
            const newId = (state.sections.length + 1).toString();
            state.sections.push({ 
                id: newId, 
                sourceContent: '', 
                targetContent: '' 
            });
            state.activeSection = newId;
        },
        updateSection: (state, action: PayloadAction<{
            id: string;
            sourceContent?: string;
            targetContent?: string;
        }>) => {
            const section = state.sections.find(s => s.id === action.payload.id);
            if (section) {
                if (action.payload.sourceContent !== undefined) {
                    section.sourceContent = action.payload.sourceContent;
                }
                if (action.payload.targetContent !== undefined) {
                    section.targetContent = action.payload.targetContent;
                }
            }
        },
        setActiveSection: (state, action: PayloadAction<string>) => {
            state.activeSection = action.payload;
        },
        setTargetLanguage: (state, action: PayloadAction<string>) => {
            state.targetLanguage = action.payload;
        },
        initializeWithText: (state, action: PayloadAction<{
            text: string;
            sourceLanguage: string;
        }>) => {
            const newSection = {
                id: (state.sections.length + 1).toString(),
                sourceContent: action.payload.text,
                targetContent: ''
            };
            state.sections.push(newSection);
            state.sourceLanguage = action.payload.sourceLanguage;
            state.activeSection = newSection.id;
        },
        deleteSection: (state, action: PayloadAction<string>) => {
            state.sections = state.sections.filter(s => s.id !== action.payload);
            if (state.activeSection === action.payload) {
                state.activeSection = state.sections[0]?.id || '1';
            }
        }
    },
    extraReducers: (builder) => {
        builder
            // Save section handling
            .addCase(saveSectionToFile.pending, (state) => {
                state.isLoading = true;
                state.error = null;
            })
            .addCase(saveSectionToFile.fulfilled, (state, action) => {
                state.isLoading = false;
                const section = state.sections.find(s => s.id === action.payload.id);
                if (section) {
                    section.filePath = action.payload.filePath;
                    section.lastModified = action.payload.lastModified;
                }
            })
            .addCase(saveSectionToFile.rejected, (state, action) => {
                state.isLoading = false;
                state.error = action.payload as string;
            })
            // Fetch sections handling
            .addCase(fetchUserSections.pending, (state) => {
                state.isLoading = true;
                state.error = null;
            })
            .addCase(fetchUserSections.fulfilled, (state, action) => {
                state.isLoading = false;
                state.sections = action.payload;
                state.activeSection = action.payload[0]?.id || '1';
            })
            .addCase(fetchUserSections.rejected, (state, action) => {
                state.isLoading = false;
                state.error = action.payload as string;
            });
    }
});

// Actions
export const {
    addSection,
    updateSection,
    setActiveSection,
    setTargetLanguage,
    initializeWithText,
    deleteSection
} = sideBySideSlice.actions;

// Selectors
export const selectSections = (state: RootState) => state.sideBySide.sections;
export const selectActiveSection = (state: RootState) => state.sideBySide.activeSection;
export const selectSourceLanguage = (state: RootState) => state.sideBySide.sourceLanguage;
export const selectTargetLanguage = (state: RootState) => state.sideBySide.targetLanguage;
export const selectActiveSectionData = (state: RootState) => 
    state.sideBySide.sections.find((section: Section) => section.id === state.sideBySide.activeSection);
export const selectIsLoading = (state: RootState) => state.sideBySide.isLoading;
export const selectError = (state: RootState) => state.sideBySide.error;

export default sideBySideSlice.reducer;