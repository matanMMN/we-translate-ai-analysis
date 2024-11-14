import { useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { selectSession, setSessionSlice } from '@/store/slices/sessionSlice';
import {fetchProjectById} from '@/actions/getUserProjects';
import { cacheProject } from '@/store/slices/projectCacheSlice';

export const useProjectRevalidation = (projectId: string) => {
    const dispatch = useDispatch();
    const session = useSelector(selectSession);

    const revalidateProject = useCallback(async () => {
        try {
            const freshProject = await fetchProjectById(projectId);
            if (freshProject) {
                dispatch(setSessionSlice({ ...session, project: freshProject }));
                dispatch(cacheProject({ projectId, project: freshProject }));
                return true;
            }
            return false;
        } catch (error) {
            console.error('Failed to revalidate project:', error);
            throw new Error('Failed to refresh project data');
        }
    }, [projectId, dispatch, session]);

    return { revalidateProject };
}; 