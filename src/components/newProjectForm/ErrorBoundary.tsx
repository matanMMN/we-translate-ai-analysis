'use client'

import { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
    children: ReactNode
}

interface State {
    hasError: boolean
}

export class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false
    }

    public static getDerivedStateFromError(): State {
        return { hasError: true }
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Uncaught error:', error, errorInfo)
    }

    public render() {
        if (this.state.hasError) {
            return (
                <div className="flex items-center justify-center min-h-screen">
                    <div className="p-6 max-w-sm mx-auto bg-white rounded-xl shadow-md">
                        <h2 className="text-xl font-bold text-red-600 mb-2">Something went wrong</h2>
                        <p className="text-gray-600 mb-4">{`We're sorry, but there was an error loading this page.`}</p>
                        <button
                            className="bg-[#1D3B34] text-white px-4 py-2 rounded hover:bg-[#1D3B34]/90 transition-colors"
                            onClick={() => this.setState({ hasError: false })}
                        >
                            Try again
                        </button>
                    </div>
                </div>
            )
        }

        return this.props.children
    }
} 