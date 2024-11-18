'use server'

import { z } from 'zod';
import { fetchMedicalTerms } from '@/services/medicalTerms';

const searchParamsSchema = z.object({
    page: z.coerce.number().default(1),
    search: z.string().optional().default(''),
    language: z.enum(['hebrew', 'english']).default('hebrew'),
});

export type SearchParams = z.infer<typeof searchParamsSchema>;

export async function getMedicalTerms(params: SearchParams) {
    try {
        const validatedParams = searchParamsSchema.parse(params);

        const data = await fetchMedicalTerms(validatedParams);
        return {
            success: true,
            data
        };
    } catch (error) {
        console.error('Server Action Error:', error);
        return {
            success: false,
            error: 'Failed to fetch medical terms'
        };
    }
}