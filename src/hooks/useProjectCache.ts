import { useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {RootState} from "@/store/store.types";
import { cacheProject, removeFromCache } from '@/store/slices/projectCacheSlice';
import {fetchProjectById} from '@/actions/getUserProjects';

export const useProjectCache = () => {
    const dispatch = useDispatch();
    const { cache, expiryTime } = useSelector((state: RootState) => state.projectCache);

    const getProjectFromCache = useCallback(async (projectId: string) => {
        const cachedProject = cache[projectId];
        
        if (cachedProject) {
            const isExpired = Date.now() - cachedProject.timestamp > expiryTime;
            
            if (!isExpired) {
                return cachedProject.data;
            }
            
            dispatch(removeFromCache(projectId));
        }

        // Fetch fresh data if not cached or expired
        const freshProject = await fetchProjectById(projectId);
        if (freshProject) {
            dispatch(cacheProject({ projectId, project: freshProject }));
        }
        return freshProject;
    }, [cache, expiryTime, dispatch]);

    return { getProjectFromCache };
}; 