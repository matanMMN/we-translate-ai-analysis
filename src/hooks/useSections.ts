import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchUserSections, selectIsLoading, selectError } from '@/store/slices/sideBySideSlice';
import { AppDispatch } from '@/store/store.types';

export const useSections = () => {
    const dispatch = useDispatch<AppDispatch>();
    const isLoading = useSelector(selectIsLoading);
    const error = useSelector(selectError);

    useEffect(() => {
        const loadSections = async () => {
            await dispatch(fetchUserSections());
        };
        
        loadSections();
    }, [dispatch]);

    return { isLoading, error };
}; 