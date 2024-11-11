import { createSlice } from '@reduxjs/toolkit';
import {RootState} from "@/store/store.types";

const initialState = {
    isOpen: true,
};

const drawerSlice = createSlice({
    name: 'drawer',
    initialState,
    reducers: {
        openDrawer: (state) => {
            state.isOpen = true;
        },
        closeDrawer: (state) => {
            state.isOpen = false;
        },
        toggleDrawer: (state) => {
            state.isOpen = !state.isOpen;
        },
    },
});


export const selectDrawer = (state: RootState) => state.drawer.isOpen

export const { openDrawer, closeDrawer, toggleDrawer } = drawerSlice.actions;
export default drawerSlice.reducer;