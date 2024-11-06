import {configureStore} from '@reduxjs/toolkit';
import themeReducer from '@/store/slices/themeSlice';
import drawerReducer from "@/store/slices/drawerSlice";
import clientLanguageReducer from '@/store/slices/clientLanguageSlice';
import sessionReducer from '@/store/slices/sessionSlice';
import projectCacheReducer from './slices/projectCacheSlice';
import sideBySideReducer from './slices/sideBySideSlice';
import projectReducer from './slices/projectSlice';

const store = configureStore({
    reducer: {
        theme: themeReducer,
        drawer: drawerReducer,
        project: projectReducer,
        clientLanguage: clientLanguageReducer,
        session: sessionReducer,
        projectCache: projectCacheReducer,
        sideBySide: sideBySideReducer,
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware({
        serializableCheck: false, // for Date type checks
    }),
});


export default store;
