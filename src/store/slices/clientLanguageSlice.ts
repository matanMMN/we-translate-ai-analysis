// copied client's language logic, almost untouched, needs a refactor


import {createAsyncThunk, createSlice} from '@reduxjs/toolkit';
import {ClientLanguages, isValidLanguage} from '@/context/LanguageContext';
import {RootState} from "@/store/store.types";
import {readFromStorage, writeToStorage} from "@/lib/storage";


export const readLanguageWithStorage = createAsyncThunk(
    'clientLanguage/readLanguageWithStorage',
    async (_, {rejectWithValue}) => {
        try {
            const initialLanguage = readFromStorage("language");
            console.log(initialLanguage)
            if (!initialLanguage) {
                writeToStorage("language", ClientLanguages.ENGLISH);
                return ClientLanguages.ENGLISH;
            }

            if (isValidLanguage(initialLanguage))
                return initialLanguage;
            else
                throw new Error("Storage language reading failed, setting to default language")

        } catch (error) {
            console.log(error);
            return rejectWithValue(ClientLanguages.ENGLISH);
        }
    }
);

const initialState = {
    // language: readFromStorage("language") || ClientLanguages.HEBREW,
    language: ClientLanguages.HEBREW,
    isRTL: false,
    isLoading: false
};

const clientLanguageSlice = createSlice({
    name: 'clientLanguage',
    initialState,
    reducers: {
        changeLanguage: (state, action) => {
            writeToStorage("language", action.payload);
            state.language = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(readLanguageWithStorage.fulfilled, (state, action) => {
                state.isLoading = false;
                state.language = action.payload as ClientLanguages;
            }).addCase(readLanguageWithStorage.pending, (state) => {
            state.isLoading = true;
        })
            .addCase(readLanguageWithStorage.rejected, (state, action) => {
                state.language = action.payload as ClientLanguages
                state.isLoading = false;
            })
    },
});


export const selectLanguage = (state: RootState) => state.clientLanguage.language;

export const {changeLanguage} = clientLanguageSlice.actions;
export default clientLanguageSlice.reducer;