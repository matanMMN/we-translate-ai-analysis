'use client'

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface ErrorBoundaryProps {
    error: Error;
    reset: () => void;
}

export function ProjectErrorBoundary({ error, reset }: ErrorBoundaryProps) {
    const router = useRouter();

    useEffect(() => {
        // Log error to your error tracking service
        console.error('Project Error:', error);
    }, [error]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-lg">
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-gray-900">Something went wrong</h2>
                    <p className="mt-2 text-sm text-gray-600">
                        {error.message || 'An unexpected error occurred'}
                    </p>
                </div>
                <div className="flex gap-4 justify-center">
                    <button
                        onClick={() => reset()}
                        className="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-hover"
                    >
                        Try again
                    </button>
                    <button
                        onClick={() => router.push('/')}
                        className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
                    >
                        Go home
                    </button>
                </div>
            </div>
        </div>
    );
} 