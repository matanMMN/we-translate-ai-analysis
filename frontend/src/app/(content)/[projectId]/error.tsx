'use client'

import { ProjectErrorBoundary } from "@/components/error/ProjectErrorBoundary";

export default function Error({
    error,
    reset,
}: {
    error: Error & { digest?: string }
    reset: () => void
}) {
    return <ProjectErrorBoundary error={error} reset={reset} />;
} 