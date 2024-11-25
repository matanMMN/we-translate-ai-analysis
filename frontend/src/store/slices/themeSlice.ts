import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Theme } from '@/context/ThemeContext.interface';
import { lightTheme, darkTheme } from '@/context/ThemeContext';
import {RootState} from "@/store/store.types";

interface ThemeState {
    theme: Theme;
}

const initialState: ThemeState = {
    theme: lightTheme,
};

const themeSlice = createSlice({
    name: 'theme',
    initialState,
    reducers: {
        toggleTheme: (state) => {
            state.theme = state.theme === lightTheme ? darkTheme : lightTheme;
        },
        setTheme: (state, action: PayloadAction<Theme>) => {
            state.theme = action.payload;
        },
    },
});




export const selectTheme = (state: RootState) => state.theme.theme

export const { toggleTheme, setTheme } = themeSlice.actions;
export default themeSlice.reducer;