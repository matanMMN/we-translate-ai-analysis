import {configureStore} from '@reduxjs/toolkit';
import themeReducer from '@/store/slices/themeSlice';
import drawerReducer from "@/store/slices/drawerSlice";
import clientLanguageReducer from '@/store/slices/clientLanguageSlice';
import projectReducer from '@/store/slices/projectSlice';
import projectCacheReducer from './slices/projectCacheSlice';
import sideBySideReducer from './slices/sideBySideSlice';

const store = configureStore({
    reducer: {
        theme: themeReducer,
        drawer: drawerReducer,
        clientLanguage: clientLanguageReducer,
        session: projectReducer,
        projectCache: projectCacheReducer,
        sideBySide: sideBySideReducer,
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware({
        serializableCheck: false, // for Date type checks
    }),
});


export default store;
