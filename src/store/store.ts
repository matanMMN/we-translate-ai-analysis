import {configureStore} from '@reduxjs/toolkit';
import themeReducer from '@/store/slices/themeSlice';
import drawerReducer from "@/store/slices/drawerSlice";
import clientLanguageReducer from '@/store/slices/clientLanguageSlice';
import projectReducer from '@/store/slices/projectSlice';

const store = configureStore({
    reducer: {
        theme: themeReducer,
        drawer: drawerReducer,
        clientLanguage: clientLanguageReducer,
        project: projectReducer
    },
});


export default store;